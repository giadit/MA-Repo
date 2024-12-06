import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
from COP_calc import eff_calc

storage_file = "results/storage_rollinghorizon.csv"
HP_file = "results/HP_rollinghorizon.csv"
ORC_file = "results/ORC_rollinghorizon.csv"
thdemand_file ="results/thdemand_rollinghorizon.csv"
el_file ="results/el_rollinghorizon.csv"

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
date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')

boolean = (el_bus["from ORC"] != 0).astype(int)
rt_eff = pd.Series(index=range(8760), dtype=float)
COP, eff = eff_calc(125, TRY=False)

for i in range(8760):
    rt_eff.iloc[i] = COP.iloc[i] * boolean.iloc[i]
    rt_eff.iloc[i] = rt_eff.iloc[i] * eff.iloc[i]
rt_eff = rt_eff[rt_eff != 0]
print(rt_eff.mean())