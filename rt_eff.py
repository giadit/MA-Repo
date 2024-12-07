import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
from COP_calc import eff_calc

# File paths
storage_file = "results/storage_rollinghorizon.csv"
HP_file = "results/HP_rollinghorizon.csv"
ORC_file = "results/ORC_rollinghorizon.csv"
thdemand_file = "results/thdemand_rollinghorizon.csv"
el_file = "results/el_rollinghorizon.csv"

# Column names
storage_names = ["SOC", "to ORC", "from HP"]
el_names = ["from ORC", "to HP", "to el_demand", "to excess", "from grid", "from PV"]
hp_names = ["from HP", "to demand", "to storage"]
orc_names = ["from storage", "to ORC", "to demand"]
demand_names = ["from HP", "from ORC", "to demand"]

# Load data
demand = pd.read_csv("results/demand.csv")
storage = pd.read_csv(storage_file, header=0, names=storage_names)
el_bus = pd.read_csv(el_file, header=0, names=el_names)
th_bus_HP = pd.read_csv(HP_file, header=0, names=hp_names)
th_bus_ORC = pd.read_csv(ORC_file, header=0, names=orc_names)
th_bus_demand = pd.read_csv(thdemand_file, header=0, names=demand_names)

# Define the date range
date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')

# Create a DataFrame for rt_eff with date_range as its index
rt_eff = pd.DataFrame(index=date_range, columns=["Efficiency"], dtype=float)

# Calculate boolean and efficiencies
boolean = (el_bus["from ORC"] != 0).astype(int)
COP, eff = eff_calc(125, TRY=False)

for i in range(8760):
    if boolean.iloc[i] != 0:
        rt_eff.iloc[i] = COP.iloc[i].item() * eff.iloc[i].item() *0.98
        print(COP.iloc[i].item(), "*", eff.iloc[i].item())
# Drop rows where the efficiency is zero (if needed)
rt_eff = rt_eff[rt_eff["Efficiency"] != 0]

# Display the first few rows
print(rt_eff.mean())

# Create the figure and plot the data
plt.figure(figsize=(12, 6))

# Plot rt_eff
plt.plot(rt_eff.index, rt_eff["Efficiency"], label="Round-Trip Efficiency", color="blue", alpha=0.8)

# Plot COP
plt.plot(date_range, COP, label="Coefficient of Performance (COP)", color="green", linestyle="--", alpha=0.8)

# Plot eff
plt.plot(date_range, eff, label="ORC Efficiency", color="red", linestyle=":", alpha=0.8)

# Customize the plot
plt.title("Round-Trip Efficiency, COP, and Efficiency Over Time", fontsize=14)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Value", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10, loc="upper right")

# Format the x-axis for better readability (optional)
from matplotlib.dates import DateFormatter
date_format = DateFormatter('%b %Y')
plt.gca().xaxis.set_major_formatter(date_format)

# Tight layout to avoid clipping
plt.tight_layout()

# Show the plot
plt.show()

rt_eff.to_csv("results/rt_eff.csv")