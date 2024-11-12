import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter

storage_names = ["SOC","to ORC","from HP"]
el_names = ["from ORC","to HP","to el_demand","to excess","from grid","from PV"]
hp_names = ["from HP","to demand","to storage"]
orc_names = ["from storage","to ORC","to demand"]
demand_names = ["from HP","from ORC","to demand"]

demand = pd.read_csv("results/demand.csv")
storage = pd.read_csv("results/storage_data.csv", header=0, names= storage_names)
el_bus = pd.read_csv("results/el_data.csv", header=0, names=el_names)
th_bus_HP = pd.read_csv("results/th_data_hp_bus.csv", header=0, names=hp_names)
th_bus_ORC = pd.read_csv("results/th_data_orc_bus.csv", header=0, names=orc_names)
th_bus_demand = pd.read_csv("results/th_data_demand_bus.csv", header=0, names=demand_names)
date_range = pd.date_range(start='2023-01-01', end='2024-01-01 00:00:00', freq='h')

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, storage["SOC"]/1000, color='#3269CC', alpha=1)
#plt.plot(date_range, el_bus["from PV"], label='PV', color='orange', alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
plt.ylim(0,185)
date_format = DateFormatter('%b. %Y')
plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('State of Charge [MWh]')

# Display the plot
plt.show()

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, th_bus_ORC["to demand"], label="to demand", color='#3269CC', alpha=1)
plt.plot(date_range, th_bus_ORC["to ORC"], label='to ORC', color='orange', alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter('%b. %Y')
plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('th. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend

plt.show()

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, el_bus["from grid"], label='from Grid', color='#3269CC', alpha=1)
plt.plot(date_range, el_bus["from ORC"], label="from ORC", color="orange", alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter('%b. %Y')
plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('el. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(date_range, th_bus_demand["from HP"], label='from HP', color='blue', alpha=0.8)
plt.plot(date_range, th_bus_demand["from ORC"], label="from TES", color="orange", alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
#date_format = DateFormatter('%b. %Y')
#plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('th. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend
plt.show()