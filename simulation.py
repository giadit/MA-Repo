import pandas as pd

import matplotlib.pyplot as plt

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

from process_results import process_results
from generate_demand import read_data, gen_heat_demand
from pv_data import fetch_pv_data
# SET PARAMS
hp_COP = 2.72125
hp_peak = 3000
orc_eff = 0.12
orc_peak = 400
storage_cap = 175000 #kWh
storage_output = 2900 #kW
storage_input = 2900 #kW
storage_eff = 0.98
storage_loss = 0.002 # 0.2 %/day


#PV data
pv_data = fetch_pv_data()

df = read_data(TRY=True)
df_temp = df["Temperature [°C]"]
# th and el demand
demand = gen_heat_demand(df_temp)
demand.to_csv("results/demand.csv")
#el prices
grid_costs = pd.read_csv("data/grid_costs.csv", skiprows=2, delimiter=";")
print(grid_costs["End User Price [EUR/kWh]"])
#Remove negative costs as they cant be processed
grid_costs[grid_costs["End User Price [EUR/kWh]"] <= 0] = 0

year_index = create_time_index(year=2023, number=len(pv_data))
energysys = solph.EnergySystem(timeindex=year_index, infer_last_interval=False)

#instantiate buses
th_hp = buses.Bus(label="th. Energy HP")
th_orc = buses.Bus(label="th. Energy ORC")
th_sink = buses.Bus(label="th. Energy Demand")
bel = buses.Bus(label="electricity")

#excess component for overproduction of electricity
excess_bel = cmp.Sink(
        label="excess_bel",
        inputs={bel: flows.Flow()})
#adding el. demand
demand_el = cmp.Sink(
        label="demand_el",
        inputs={bel: flows.Flow(fix= demand["demand_el"], nominal_value = 1)})
#adding th. demand
demand_th = cmp.Sink(
        label="demand_th",
        inputs={th_sink: flows.Flow(fix= demand["MFH"], nominal_value = 1)})
#bridge for ORC
bridgeORC = cmp.Converter(
        label = "bridgeORC",
        inputs={th_orc: flows.Flow() },
        outputs={th_sink: flows.Flow()},
        conversion_factors={th_orc:1})
#bridge for HP
bridgeHP = cmp.Converter(
        label = "bridgeHP",
        inputs={th_hp: flows.Flow()},
        outputs={th_sink: flows.Flow()},
        conversion_factors={th_hp: 1})
#create grid
grid = cmp.Source(
        label="grid",
        outputs={bel: flows.Flow(variable_costs=grid_costs["End User Price [EUR/kWh]"])})
#fixed source for pv
pv = cmp.Source(
        label="pv",
        outputs={bel: flows.Flow(fix=pv_data, nominal_value=1)})
#adding converter (HeatPump)
HP = cmp.Converter(
        label = "HP",
        inputs={bel: flows.Flow(nominal_value=1, max=hp_peak/hp_COP)},
        outputs={th_hp: flows.Flow()},
        conversion_factors={th_hp: hp_COP}) # technikkatalog
#adding storage system
storage = cmp.GenericStorage(
        nominal_storage_capacity= storage_cap,
        label = "storage",
        inputs = {th_hp: flows.Flow(nominal_value= storage_input)},
        outputs = {th_orc: flows.Flow(nominal_value= storage_output)},
        loss_rate = storage_loss/24,
        initial_storage_level = None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=storage_eff)
#adding converter (ORC)
ORC = cmp.Converter(
        label = "ORC",
        inputs={th_orc: flows.Flow(nominal_value=1, max=orc_peak/orc_eff)},
        outputs={bel: flows.Flow()},
        conversion_factors={bel: orc_eff})
#add nodes to system
energysys.add(th_hp, th_orc, th_sink,
             bel, excess_bel,
             demand_th, demand_el,
             grid, pv,
             bridgeHP, bridgeORC,
             ORC, HP, storage)
#energysys.add(th_hp, th_orc,
#              bel, excess_bel,
#              demand_el,
#              grid, pv,
#              ORC, HP, storage)

#create optimization
om = solph.Model(energysys)
om.solve(solver='cbc', solve_kwargs={'tee': True})
om.write('my_model.lp', io_options={'symbolic_solver_labels': True})

#processing results
energysys.results = processing.results(om)
results = solph.processing.results(om)
total_cost = om.objective()
print("Total cost of the optimization:", total_cost)

process_results(results)