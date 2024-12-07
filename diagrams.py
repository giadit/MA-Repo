import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
from pv_data import fetch_pv_data
from COP_calc import eff_calc

storage_file = "results/storage_rollinghorizon.csv"
HP_file = "results/HP_rollinghorizon.csv"
ORC_file = "results/ORC_rollinghorizon.csv"
thdemand_file ="results/thdemand_rollinghorizon.csv"
el_file ="results/el_rollinghorizon.csv"
elc_file = "results/el_bus_recalc_PTES_2023.csv"

storage_names = ["SOC","to ORC","from HP"]
el_names = ["from ORC","to HP","to el_demand","to excess","from grid","from PV"]
hp_names = ["from HP","to demand","to storage"]
orc_names = ["from storage","to ORC","to demand"]
demand_names = ["from HP","from ORC","to demand"]

demand = pd.read_csv("results/demand.csv")
storage = pd.read_csv(storage_file, header=0, names=storage_names)
el_bus = pd.read_csv(el_file, header=0, names=el_names)
th_bus_HP = pd.read_csv(HP_file, header=0, names=hp_names)
th_bus_ORC = pd.read_csv(ORC_file, header=0, names=orc_names)
th_bus_demand = pd.read_csv(thdemand_file, header=0, names=demand_names)
el_bus_c = pd.read_csv(elc_file, delimiter=";", index_col=0)
grid_costs = pd.read_csv("data/grid_costs.csv", skiprows=2, delimiter=";")
grid_costs[grid_costs["End User Price [EUR/kWh]"] <= 0] = 0
pv_data = fetch_pv_data(2023)

date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')
colors = ["blue", "green", "orange"]
#monthly use
monthly_el_grid = el_bus_c["grid to demand"].to_frame().set_index(date_range).resample("ME").sum()
monthly_el_PV = el_bus_c["pv to demand"].to_frame().set_index(date_range).resample("ME").sum()
monthly_el_ORC = el_bus["from ORC"].to_frame().set_index(date_range).resample("ME").sum()

# Combine all monthly data into one DataFrame
monthly_data = pd.concat(
    [monthly_el_grid["grid to demand"], monthly_el_PV["pv to demand"], monthly_el_ORC["from ORC"]],
    axis=1,
    keys=['Grid', 'PV', 'ORC']
)

# Plot the data as a grouped bar graph
fig, ax1 = plt.subplots(figsize=(12, 6))
monthly_data.plot(kind='bar', ax=ax1, width=0.8, color=colors)

# Customize the bar graph
ax1.set_ylabel("el. Energy [kWh]")
ax1.set_xlabel("Month")
ax1.set_xticks(range(12))
ax1.set_xticklabels(monthly_data.index.strftime('%B'), rotation=45)
ax1.legend(title="Source:")
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_title('Monthly Electrical Energy Distribution', fontsize=14)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()

# Define labels and values
labels = ["Grid", "PV", "ORC"]
values = [el_bus_c["grid to demand"].sum(), el_bus_c["pv to demand"].sum(), el_bus["from ORC"].sum()]

# Plot the pie chart
fig, ax2 = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax2.pie(
    values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
    textprops={'fontsize': 12}
)

# Style the autopct text (percentage inside pie slices)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_weight('bold')

# Add a title to the pie chart
ax2.set_title("Breakdown of Sources", fontsize=14, pad=20)

# Add a legend outside the pie chart
ax2.legend(
    wedges, labels, title="Sources of electricity", loc="center left",
    bbox_to_anchor=(1, 0.5), fontsize=10
)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()


# Create the figure and axis
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 6))
ax1.plot(date_range,th_bus_demand["to demand"], 'r-')
ax1.set_ylabel("th. Demand [kW]")
ax1.grid()
ax1.set_ylim(0, th_bus_demand["to demand"].max() * 1.1)
ax2.plot(date_range, pv_data["p_mp"], 'g-', alpha = 0.8, label = "PV Production")
ax2.plot(date_range, el_bus["to el_demand"], "orange", alpha = 0.8, label= "el. Demand")
ax2.set_ylabel('El. Energy [kW]')
ax2.grid()
ax2.legend()
ax2.set_ylim(0,pv_data["p_mp"].max()* 1.1)
# Plot the State of Charge (SOC)
ax3.plot(date_range, storage["SOC"]/1000, color='blue')
ax3.set_ylabel('Energy Stored [MWh]')
ax3.grid()
ax3.set_ylim(0, (storage["SOC"] / 1000).max() * 1.1)
# Set axis limits
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
# Format the x-axis for better readability
date_format = DateFormatter('%b %Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
#date_format = DateFormatter("%d/%m/%y %H:%M")
#plt.gca().xaxis.set_major_formatter(date_format)
# Show the plot
plt.tight_layout()
plt.show()

#el. Sources + Price
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
ax2.plot(date_range, th_bus_ORC["to demand"], label="TES", color="red", linewidth=2, alpha=0.8)
ax2.plot(date_range, el_bus["from ORC"], label="ORC", color=colors[2], linewidth=2, alpha=1)
ax2.set_ylabel("th./el. Energy [kW]")
ax2.grid()
ax2.legend()
ax2.set_ylim(0,th_bus_ORC["to demand"].max())
ax1.plot(date_range,storage["SOC"]/1000, 'blue')
ax1.set_ylabel("Energy Stored [MWh]")
ax1.grid()
ax1.set_ylim(0,(storage["SOC"]/1000).max())
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter("%d/%m/%y")
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()


#el. Sources + Price
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
ax2.plot(date_range, el_bus_c["grid to demand"], label="Grid", color=colors[0], linewidth=2, alpha=0.8)
ax2.plot(date_range, el_bus_c["pv to demand"], label="PV", color=colors[1], linewidth=2, alpha=0.8)
ax2.plot(date_range, el_bus["from ORC"], label="ORC", color=colors[2], linewidth=2, alpha=1)
ax2.set_ylabel("el. Energy [kW]")
ax2.grid()
ax2.legend()
ax2.set_ylim(0,el_bus_c["grid to demand"].max())
ax1.plot(date_range,grid_costs["End User Price [EUR/kWh]"], 'r-')
ax1.set_ylabel("el. Price [EUR/kWh]")
ax1.grid()
ax1.set_ylim(0,grid_costs["End User Price [EUR/kWh]"].max())
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter("%d/%m/%y")
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()

# Create the figure and axis
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
ax1.plot(date_range,grid_costs["End User Price [EUR/kWh]"], 'orange')
ax1.set_ylabel("El. Price [EUR/kWh]")
ax1.grid()
ax1.set_ylim(0,grid_costs["End User Price [EUR/kWh]"].max())
ax2.plot(date_range, th_bus_demand["from ORC"], 'r-', alpha=0.8, label= "from storage")
ax2.plot(date_range, th_bus_demand["from HP"], 'b-', alpha=0.8, label="from HP")
ax2.set_ylabel('th. Energy [kW]')
ax2.grid()
ax2.set_ylim(0,th_bus_demand["from ORC"].max()*1.1)
# Set axis limits
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter("%d/%m/%y")
plt.gca().xaxis.set_major_formatter(date_format)
# Format the x-axis for better readability
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

# Show the plot
plt.tight_layout()
plt.legend()
plt.show()

# Combine sums into a list or Series
labels = ["ORC", "th. Demand"]
values = [th_bus_ORC["to ORC"].sum(), th_bus_ORC["to demand"].sum()]

# Plot the pie chart
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=["orange", "red"],
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
    textprops={'fontsize': 12}
)

# Style the autopct text (percentage inside pie slices)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_weight('bold')

# Add a title with custom styling
#plt.title( "Proportions of Summed DataFrames",fontsize=16,fontweight='bold',pad=20)

# Add a legend outside the pie chart
plt.legend(wedges, labels, title="TES Energy Share [kW]", bbox_to_anchor=(1, 0.5), fontsize=12)

# Display the chart
plt.tight_layout()
plt.show()

# Excess Electrical Energy
plt.figure(figsize=(12, 7))
# Plot the excess electrical energy
plt.plot(date_range, el_bus["to excess"], label="Excess Electricity", color='#1f77b4', linewidth=2, alpha=0.8)
# Set axis limits
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
# Format the x-axis for better readability
date_format = DateFormatter('%b %Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
# Adding labels, title, and legend
plt.title('Excess Electrical Energy Throughout the Year', fontsize=14, fontweight='bold')
plt.ylabel('Excess Electrical Energy [kW]', fontsize=12)
plt.xlabel('Date', fontsize=12)
plt.legend(fontsize=10, loc='upper right')  # Adjust legend position and size
# Add a grid for better readability
plt.grid(visible=True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print(el_bus["to excess"].sum())