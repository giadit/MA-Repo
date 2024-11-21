import pandas as pd

df = pd.read_csv("data/TRY2045_525246_133946_Jahr.csv")
# Select specific columns
data = df[["D","B","t","WG"]]
# Rename the columns dhi,dni,ghi,temp_air,wind_speed
data = data.rename(columns={
    "D": "dhi", "B": 'dni', "t": "temp_air",
"WG": "wind_speed"})

print(data)
data.to_csv("data/pv_data_2045.csv")