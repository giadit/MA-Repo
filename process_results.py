import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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



def process_results(results):
    # get all variables of a specific component/bus
    custom_storage = views.node(results, "storage")
    thermal_bus_orc = views.node(results, "th. Energy ORC")
    thermal_bus_hp = views.node(results, "th. Energy HP")
    thermal_bus_demand = views.node(results, "th. Energy Demand")
    electricity_bus = views.node(results, "electricity")

    # save to csv
    custom_storage["sequences"].to_csv("results/storage_data.csv")
    electricity_bus["sequences"].to_csv("results/el_data.csv")
    thermal_bus_orc["sequences"].to_csv(("results/th_data_orc_bus.csv"))
    thermal_bus_hp["sequences"].to_csv(("results/th_data_hp_bus.csv"))
    #thermal_bus_demand["sequences"].to_csv(("results/th_data_demand_bus.csv"))
    # plot the time series (sequences) of a specific component/bus
    # How to access individual series:
    #electricity_bus['sequences'][(('electricity_bus', 'demand'), 'flow')]

    #plot storage SOC

   #fig, ax = plt.subplots(figsize=(10, 5))
   #custom_storage['sequences'][(('storage', 'None'), 'storage_content')].plot(
   #   ax=ax, kind="line", drawstyle="steps-post", colormap = "bwr"
   #)
   #plt.title('State of Charge')
   #plt.ylabel('Power [kW]')
   #
   #fig.subplots_adjust(top=0.8)
   #plt.savefig("results/storage_SOC.png", dpi=600)
   #plt.show()
   #
   #fig, ax = plt.subplots(figsize=(10, 5))
   #custom_storage["sequences"].iloc[:, 1:3].plot(
   #    ax=ax, kind="line", drawstyle="steps-post"
   #)
   #plt.legend(
   #    loc="upper center",
   #    prop={"size": 8},
   #    bbox_to_anchor=(0.5, 1.25),
   #    ncol=2,
   #)
   #fig.subplots_adjust(top=0.8)
   #plt.savefig("results/storage_data.png", dpi=300)
   #plt.show()
   #
   # # plot electricity demand
   #fig, ax1 = plt.subplots(figsize=(10, 6))
   #
   #ORC_el = electricity_bus["sequences"].iloc[:, 0]  # Column at index 0 for the first bar
   #grid_el = electricity_bus["sequences"].iloc[:, 4]  # Column at index 4 for the second bar
   #demand_el = electricity_bus["sequences"].iloc[:, 2]  # Column at index 2 for the line plot
   #
   # # Plot the stacked bars
   #bar1 = ax1.bar(electricity_bus["sequences"].index, ORC_el, label='ORC el.', color='yellow', width=2)
   #bar2 = ax1.bar(electricity_bus["sequences"].index, grid_el, bottom=ORC_el, label='Grid el.', color='orange', width=2)
   #
   # # Plot the line plot
   #ax1.plot(electricity_bus["sequences"].index, demand_el, label='el. Demand', color='lightgreen', marker=None, linewidth=1)
   #
   #ax1.set_ylabel('Power [kW]')
   #ax1.legend()
   #
   ## Improve layout
   ## Generate 24 evenly spaced tick positions along the x-axis
   #tick_positions = np.linspace(0, len(electricity_bus["sequences"].index) - 1, 24).astype(int)
   #
   ## Set x-axis ticks to the calculated positions
   #ax1.set_xticks(electricity_bus["sequences"].index[tick_positions])
   #
   ## Format the tick labels to show the date, rotating for readability
   #ax1.set_xticklabels(electricity_bus["sequences"].index[tick_positions].strftime('%Y-%m-%d'), rotation=45)
   #
   #
   #plt.tight_layout()
   #plt.savefig("results/el_data.png", dpi=600)
   #plt.show()
   #
   ## plot electricity from grid & PV
   #fig, ax = plt.subplots(figsize=(10, 5))
   #electricity_bus["sequences"].iloc[:, 4:6].plot(
   #    ax=ax, kind="line", drawstyle="steps-post"
   #)
   #plt.legend(["Grid","PV"],
   #    loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
   #)
   #fig.subplots_adjust(top=0.8)
   #plt.savefig("results/grid_pv_data.png", dpi=600)
   #plt.show()
   #
   ## plot excess
   #fig, ax = plt.subplots(figsize=(10, 5))
   #electricity_bus["sequences"].iloc[:, 3].plot(
   #    ax=ax, kind="line", drawstyle="steps-post"
   #)
   #plt.title('Excess Power')
   #plt.ylabel('Power [kW]')
   #
   #fig.subplots_adjust(top=0.8)
   #plt.savefig("results/excess_data.png", dpi=300)
   #plt.show()

    return
