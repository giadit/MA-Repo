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
    thermal_bus = views.node(results, "th. Energy")
    electricity_bus = views.node(results, "electricity")
    print(thermal_bus)

    # Convert to pandas DataFrame
    electricity_df = pd.DataFrame({
        'Demand': electricity_bus['sequences'][(('electricity', 'demand_el'), 'flow')],
        'Excess': electricity_bus['sequences'][(('electricity', 'demand_el'), 'flow')],
        "ORC": electricity_bus['sequences'][(('ORC', 'electricity'), 'flow')],
        'HP': electricity_bus['sequences'][(("electricity", 'HP'), 'flow')]
    })
    # Set the plot size
    plt.figure(figsize=(12, 6))

    # Plot the electricity demand
    plt.plot(electricity_df.index, electricity_df['Demand'], label='Electricity Demand', color='blue')

    # Plot the electricity generation
    plt.plot(electricity_df.index, electricity_df['Generation'], label='Electricity Generation', color='green')

    # Plot the electricity storage
    plt.plot(electricity_df.index, electricity_df['Storage'], label='Electricity Storage', color='orange')

    # Add title and labels
    plt.title('Energy System Results')
    plt.xlabel('Time')
    plt.ylabel('Power [MW]')

    # Add legend
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add grid
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    # save to csv
    custom_storage["sequences"].to_csv("storage_data.csv")
    electricity_bus["sequences"].to_csv("el_data.csv")
    # plot the time series (sequences) of a specific component/bus
    fig, ax = plt.subplots(figsize=(10, 5))
    custom_storage["sequences"].iloc[:, 0].plot(
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
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(
        loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
    )
    fig.subplots_adjust(top=0.8)
    plt.savefig("results/demand_data.png", dpi=300)
    plt.show()

    # plot electricity from grid & PV
    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].iloc[:, 4:6].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(
        loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
    )
    fig.subplots_adjust(top=0.8)
    plt.savefig("results/grid_pv_data.png", dpi=300)
    plt.show()

    # plot excess
    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].iloc[:, 3].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(
        loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
    )
    fig.subplots_adjust(top=0.8)
    plt.savefig("results/excess_data.png", dpi=300)
    plt.show()

