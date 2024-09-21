import pandas as pd
import matplotlib.pyplot as plt

hourly_index = pd.date_range(start="2023-01-01 00:00:00", end="2023-12-31 23:00:00", freq='h')
df_pv = pd.read_csv("data/pv_data_2023.csv")
df_pv.index = hourly_index

df_pv.to_csv("data/pvlib_berlin_2023.csv")