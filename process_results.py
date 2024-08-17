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



def process_results(results):
    # get all variables of a specific component/bus
    custom_storage = views.node(results, "storage")
    thermal_bus_orc = views.node(results, "th. Energy ORC")
    thermal_bus_hp = views.node(results, "th. Energy HP")
    electricity_bus = views.node(results, "electricity")

    # save to csv
    custom_storage["sequences"].to_csv("results/storage_data.csv")
    electricity_bus["sequences"].to_csv("results/el_data.csv")
    thermal_bus_orc["sequences"].to_csv(("results/th_data_orc_bus.csv"))
    thermal_bus_hp["sequences"].to_csv(("results/th_data_hp_bus.csv"))

    # plot the time series (sequences) of a specific component/bus
    # How to access individual series:
    #electricity_bus['sequences'][(('electricity_bus', 'demand'), 'flow')]

    #plot storage SOC

    fig, ax = plt.subplots(figsize=(10, 5))
    custom_storage['sequences'][(('storage', 'None'), 'storage_content')].plot(
       ax=ax, kind="line", drawstyle="steps-post", colormap = "bwr"
    )
    plt.title('State of Charge')
    plt.ylabel('Power [kW]')

    fig.subplots_adjust(top=0.8)
    plt.savefig("results/storage_SOC.png", dpi=1200)
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    custom_storage["sequences"].iloc[:, 1:3].plot(
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

    # plot electricity demand
    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].iloc[:, 2].plot(
        ax=ax, kind="line", drawstyle="steps-post")

    plt.title('El. Demand')
    plt.ylabel('Power [kW]')

    fig.subplots_adjust(top=0.8)
    plt.savefig("results/demand_data.png", dpi=1200)
    plt.show()

    # plot electricity from grid & PV
    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].iloc[:, 4:6].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(["Grid","PV"],
        loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
    )
    fig.subplots_adjust(top=0.8)
    plt.savefig("results/grid_pv_data.png", dpi=1200)
    plt.show()

    # plot excess
    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].iloc[:, 3].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.title('Excess Power')
    plt.ylabel('Power [kW]')

    fig.subplots_adjust(top=0.8)
    plt.savefig("results/excess_data.png", dpi=300)
    plt.show()

    return
