import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter

#TES_file = "results/battery/TES_results.csv"
battery_file = "results/battery/battery_results.csv"
thdemand_file = "results/battery/th_results.csv"
el_file = "results/battery/el_results.csv"

#TES_names = ["SOC","from TES","to TES"]
battery_names = ["SOC","from battery","to battery"]
th_names = ["from HP","to demand"]
el_names = ["from battery","to HP","to battery","to_demand","to excess","from grid","from PV"]

#TES = pd.read_csv(TES_file, header=0, names=TES_names)
el_bus = pd.read_csv(el_file, header=0, names=el_names)
th_bus = pd.read_csv(thdemand_file, header=0, names=th_names)
battery = pd.read_csv(battery_file, header=0, names=battery_names)
date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, battery["SOC"]/1000, color='#3269CC', alpha=1)
#plt.plot(date_range, el_bus["from PV"], label='PV', color='orange', alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
plt.ylim(0,battery["SOC"].max()*1.1/1000)
date_format = DateFormatter('%b. %Y')
#plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('State of Charge [MWh]')

# Display the plot
plt.show()


# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, el_bus["to excess"], label="to excess", color='#3269CC', alpha=1)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter('%b. %Y')
plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('Excess el. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend

plt.show()

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, el_bus["from grid"], label='from Grid', color='#3269CC', alpha=1)
plt.plot(date_range, el_bus["from battery"], label="from battery", color="orange", alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
date_format = DateFormatter('%b. %Y')
plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('el. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(date_range, th_bus["from HP"], label='from HP', color='blue', alpha=0.8)
#plt.plot(date_range, th_bus["from TES"], label="from TES", color="orange", alpha=0.7)
plt.xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31 23:00:00'))
#date_format = DateFormatter('%b. %Y')
#plt.gca().xaxis.set_major_formatter(date_format)
# Adding labels and title
plt.xticks(rotation=45)
plt.ylabel('th. Energy [kW]')
plt.legend()  # Adds the custom labels to the legend
plt.show()