import matplotlib.pyplot as plt
import pandas as pd

import oemof.solph as solph
from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import helpers
from oemof.solph import processing
from oemof.solph import views

from oemof_visio import plot
from oemof_visio.energy_system_graph import ESGraphRenderer


from generate_demand import read_data, gen_heat_demand

#to be removed later, now for PV and Wind
data = pd.read_csv("basic_example.csv")

df = read_data(TRY=True)
df_temp = df["Temperature [°C]"]
# th and el demand
demand = gen_heat_demand(df_temp)
#el prices
grid_costs = pd.read_csv("data/grid_costs.csv", skiprows=2)
#Remove negative costs as they cant be processed
grid_costs[grid_costs["Preis (EUR/kWh)"] <= 0] = 0

year_index = create_time_index(year=2023, number=len(data))
energysys = solph.EnergySystem(timeindex=year_index, infer_last_interval=False)

#generate buses
th1 = buses.Bus(label="th. Energy HP")
th2 = buses.Bus(label="th. Energy ORC")
bel = buses.Bus(label="electricity")

#excess component for overproduction of el
excess_bel = cmp.Sink(
        label="excess_bel",
        inputs={bel: flows.Flow()})
#adding el demand
demand_el = cmp.Sink(
        label="demand_el",
        inputs={bel: flows.Flow(fix= demand["demand_el"], nominal_value = 1)})
#adding th demand
demand_th = cmp.Sink(
        label="demand_th",
        inputs={th2: flows.Flow(fix= demand["MFH"], nominal_value = 1)})
#create grid
grid = cmp.Source(
        label="grid",
        outputs={bel: flows.Flow(variable_costs=grid_costs["Preis (EUR/kWh)"])})
#fixed source for pv
pv = cmp.Source(
        label="pv",
        outputs={bel: flows.Flow(fix=data["pv"], nominal_value=582000)})
#create convereter (HeatPump)
HP = cmp.Converter(
        label = "HP",
        inputs={bel: flows.Flow()},
        outputs={th1: flows.Flow()},
        conversion_factors={th1: 3})
#create storage system
storage = cmp.GenericStorage(
        nominal_storage_capacity=10077997,
        label = "storage",
        inputs = {th1: flows.Flow(nominal_value=1007797/6)},
        outputs = {th2: flows.Flow(nominal_value=1007797/6, variable_costs=0.001)},
        loss_rate = 0.00,
        initial_storage_level = None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.9)
#create convereter (ORC)
ORC = cmp.Converter(
        label = "ORC",
        inputs={th2: flows.Flow()},
        outputs={bel: flows.Flow()},
        conversion_factors={bel: 0.15})
#add nodes to system
energysys.add(th1,th2,bel,
              excess_bel,demand_th,demand_el,grid,pv,
              ORC, HP, storage)

#create optimization
om = solph.Model(energysys)
om.solve(solver='cbc', solve_kwargs={'tee': True})
om.write('my_model.lp', io_options={'symbolic_solver_labels': True})
energysys.results = processing.results(om)
results = solph.processing.results(om)

# get all variables of a specific component/bus
custom_storage = views.node(results, "storage")
electricity_bus = views.node(results, "electricity")

#save to csv
custom_storage["sequences"].to_csv("storage_data.csv")
electricity_bus["sequences"].to_csv("el_data.csv")
# plot the time series (sequences) of a specific component/bus
fig, ax = plt.subplots(figsize=(10, 5))
custom_storage["sequences"].iloc[:,0].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center",
    prop={"size": 8},
    bbox_to_anchor=(0.5, 1.25),
    ncol=2,
)
fig.subplots_adjust(top=0.8)
plt.savefig("results/storage_SOC.png", dpi=300)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
custom_storage["sequences"].iloc[:,1:3].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center",
    prop={"size": 8},
    bbox_to_anchor=(0.5, 1.25),
    ncol=2,
)
fig.subplots_adjust(top=0.8)
plt.savefig("results/storage_data.png", dpi=300)
plt.show()


#plot electricity demand
fig, ax = plt.subplots(figsize=(10, 5))
electricity_bus["sequences"].iloc[:,2].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.savefig("results/demand_data.png", dpi=300)
plt.show()

#plot electricity from grid & PV
fig, ax = plt.subplots(figsize=(10, 5))
electricity_bus["sequences"].iloc[:,4:6].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.savefig("results/grid_pv_data.png", dpi=300)
plt.show()


#plot excess
fig, ax = plt.subplots(figsize=(10, 5))
electricity_bus["sequences"].iloc[:,3].plot(
    ax=ax, kind="line", drawstyle="steps-post"
)
plt.legend(
    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
)
fig.subplots_adjust(top=0.8)
plt.savefig("results/excess_data.png", dpi=300)
plt.show()

