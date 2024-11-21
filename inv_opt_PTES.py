import pandas as pd
import matplotlib.pyplot as plt
import oemof.solph as solph
from oemof.solph import EnergySystem, Model, buses, components as cmp, create_time_index, flows, processing
from oemof.solph import views
from oemof.tools import economics
import pprint as pp


from process_results import process_results
from extr_inv import extract_investment
from generate_demand import read_data, gen_heat_demand
from pv_data import fetch_pv_data
from COP_calc import eff_calc
# SET PARAMS
hp_COP = 3.21375
hp_peak = 3000
orc_eff = 0.15
orc_peak = 400
storage_cap = 175000  # kWh
storage_output = 2900  # kW
storage_input = 2900  # kW
storage_eff = 0.98
storage_loss = 0.002  # 0.2 %/day
COP, eta = eff_calc(125, TRY = False)

epc_storage = economics.annuity(capex=3.3,n=40,wacc=0.05)
epc_HP = economics.annuity(capex=782, n=30,wacc=0.05)
epc_ORC = economics.annuity(capex=2880,n=30,wacc=0.05)


yearly_costs = 0
hour_interval = int(8760/1)
# Load Data
pv_data = fetch_pv_data(2023)
df = read_data(TRY=False)
df_temp = df["Temperature [°C]"]
demand = gen_heat_demand(df_temp)
grid_costs = pd.read_csv("data/grid_costs.csv", skiprows=2, delimiter=";")
grid_costs[grid_costs["End User Price [EUR/kWh]"] <= 0] = 0

# Create Full-Year Time Index and Weekly Intervals
year_index = create_time_index(year=2023, number=len(pv_data)-1)
weeks = [year_index[i:i + hour_interval] for i in range(0, len(year_index), hour_interval)]  # 168 hours per week
# Set up initial storage level
initial_storage_level = None  # 50% full at the start
#set index the same
pv_data.set_index(year_index)
demand.set_index(year_index)
grid_costs.set_index(year_index)
COP.set_index(year_index)
eta.set_index(year_index)
#create slices
slices = []

storage_results = pd.DataFrame()
ORC_results = pd.DataFrame()
HP_results = pd.DataFrame()
thdemand_results = pd.DataFrame()
el_results = pd.DataFrame()

for i in range(0, 8760, hour_interval):
    slices.append(i)
# Loop through each week and run optimization
for week_idx, week in enumerate(weeks):
    print(f"Optimizing Slice {week_idx + 1}")

    # Subset data for the current week
    week_pv_data = pv_data["p_mp"][slices[week_idx]:slices[week_idx]+hour_interval+1].reset_index(drop=True)
    week_demand_el = demand["demand_el"][slices[week_idx]:slices[week_idx]+hour_interval+1].reset_index(drop=True)
    week_demand_th = demand["MFH"][slices[week_idx]:slices[week_idx]+hour_interval+1].reset_index(drop=True)
    week_grid_costs = grid_costs["End User Price [EUR/kWh]"][slices[week_idx]:slices[week_idx]+hour_interval+1].reset_index(drop=True)

    # Create weekly energy system
    energysys = solph.EnergySystem(timeindex=week, infer_last_interval=True)

    # Define buses
    th_hp = buses.Bus(label="th. Energy HP")
    th_orc = buses.Bus(label="th. Energy ORC")
    th_sink = buses.Bus(label="th. Energy Demand")
    bel = buses.Bus(label="electricity")

    # Add components (similar to your original setup)
    excess_bel = cmp.Sink(label="excess_bel", inputs={bel: flows.Flow()})
    demand_el = cmp.Sink(label="demand_el", inputs={bel: flows.Flow(fix=week_demand_el, nominal_value=1)})
    demand_th = cmp.Sink(label="demand_th", inputs={th_sink: flows.Flow(fix=week_demand_th, nominal_value=1)})

    bridgeORC = cmp.Converter(label="bridgeORC", inputs={th_orc: flows.Flow()}, outputs={th_sink: flows.Flow()},
                              conversion_factors={th_orc: 1})
    bridgeHP = cmp.Converter(label="bridgeHP", inputs={th_hp: flows.Flow()}, outputs={th_sink: flows.Flow()},
                             conversion_factors={th_hp: 1})

    grid = cmp.Source(label="grid", outputs={bel: flows.Flow(variable_costs=week_grid_costs)})
    pv = cmp.Source(label="pv", outputs={bel: flows.Flow(fix=week_pv_data, nominal_value=1)})

    HP = cmp.Converter(label="HP", inputs={bel: flows.Flow()},
                       outputs={th_hp: flows.Flow(nominal_value=solph.Investment(ep_costs=epc_HP))},
                       conversion_factors={th_hp: COP["COP"]})


    # Configure storage with rolling initial level
    storage = cmp.GenericStorage(
        #nominal_storage_capacity=storage_cap,
        label="storage",
        inputs={th_hp: flows.Flow(nominal_value=storage_input)},
        outputs={th_orc: flows.Flow(nominal_value=storage_output)},
        loss_rate=storage_loss / 24,
        initial_storage_level=initial_storage_level, balanced=True,
        inflow_conversion_factor=1,
        outflow_conversion_factor=storage_eff,
        investment= solph.Investment(ep_costs=epc_storage)
    )

    ORC = cmp.Converter(label="ORC",
                        inputs={th_orc: flows.Flow()},
                        outputs={bel: flows.Flow(nominal_value=solph.Investment(ep_costs=epc_ORC))},
                        conversion_factors={bel: eta["Efficiency"]})

    # Add components to energy system
    energysys.add(th_hp, th_orc, th_sink, bel, excess_bel, demand_th, demand_el, grid, pv, bridgeHP, bridgeORC, ORC, HP, storage)

    # Optimization model for the week
    om = Model(energysys)
    om.solve(solver='cbc', solve_kwargs={'tee': True})

    # Process results for the current week
    #energysys.results = processing.results(om)
    results = solph.processing.results(om)
    total_cost = om.objective()
    print(f"Total cost for Slice {week_idx + 1}: {total_cost}")
    yearly_costs += total_cost

    # Process and analyze results as needed
    custom_storage = views.node(results, "storage")["sequences"]
    thermal_bus_orc = views.node(results, "th. Energy ORC")["sequences"]
    thermal_bus_hp = views.node(results, "th. Energy HP")["sequences"]
    thermal_bus_demand = views.node(results, "th. Energy Demand")["sequences"]
    electricity_bus = views.node(results, "electricity")["sequences"]

    storage_results = pd.concat([storage_results, custom_storage.iloc[:-1]])
    HP_results = pd.concat([HP_results, thermal_bus_hp.iloc[:-1]])
    ORC_results = pd.concat([ORC_results, thermal_bus_orc.iloc[:-1]])
    thdemand_results = pd.concat([thdemand_results, thermal_bus_demand.iloc[:-1]])
    el_results = pd.concat([el_results, electricity_bus.iloc[:-1]])

    # Update initial storage level for the next week
    initial_storage_level = custom_storage.iloc[-2,0] / storage_cap  # Normalize to capacity

    # Extract investments for storage, HP, and ORC
    storage_investment = extract_investment(results=results, component_label="storage")
    hp_investment = extract_investment(results=results, component_label="HP")
    orc_investment = extract_investment(results=results, component_label="ORC")

    # Annualized costs
    storage_annual_cost = epc_storage * storage_investment
    hp_annual_cost = epc_HP * hp_investment
    orc_annual_cost = epc_ORC * orc_investment

    # Log results
    print(f"Week {week_idx + 1} - Investments and Capacities:")
    print(f"  Storage investment (kWh): {storage_investment}, Cost: €{storage_annual_cost:.2f}")
    print(f"  HP investment (kW): {hp_investment}, Cost: €{hp_annual_cost:.2f}")
    print(f"  ORC investment (kW): {orc_investment}, Cost: €{orc_annual_cost:.2f}")
    print(f"  Total Cost : €{yearly_costs:.2f}")

storage_results.to_csv("results/storage_rollinghorizon.csv")
ORC_results.to_csv("results/ORC_rollinghorizon.csv")
HP_results.to_csv("results/HP_rollinghorizon.csv")
thdemand_results.to_csv("results/thdemand_rollinghorizon.csv")
el_results.to_csv("results/el_rollinghorizon.csv")

