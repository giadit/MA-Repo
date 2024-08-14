import pandas as pd
from generate_heat_demand import gen_heat_demand

def read_data(TRY):

    if TRY:
        df = pd.read_csv("data/TRY2045_525246_133946_Jahr.csv")
        # Select specific columns
        data = df[["t", "p","B","D"]]
        # Rename the columns
        data = data.rename(columns={
            "t": "Temperature [°C]", "p": 'Pressure [hPa]', "B": "dir. Strahlung [W/m2]",
        "D": "diff. Strahlung [W/m2]"})

        date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')

        data = data.set_index(date_range)
    else:
        data = pd.read_csv("data/t_data_2023.csv")
    return data

df = read_data(TRY=True)
df_temp = df["Temperature [°C]"]
demand = gen_heat_demand(df_temp)
print(demand)