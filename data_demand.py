import pandas as pd
from generate_demand import gen_heat_demand
from generate_demand import read_data
from feedinlib import powerplants #Photovoltaic
from feedinlib import models #Pvlib


df = read_data(TRY=True)
df_temp = df["Temperature [°C]"]
demand = gen_heat_demand(df_temp)
print(demand)