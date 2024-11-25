import pandas as pd

df = pd.read_csv("data/energy-charts_Stromproduktion_und_Börsenstrompreise_in_Deutschland_2019.csv", delimiter=";", index_col=0)

corr = {"1": 92.0315557,
        "2": 122.6917515,
        "3": 91.64550672,
        "4":66.98597083,
        "5":42.38581989,
        "6":34.06513889,
        "7":37.4812043,
        "8":55.93759812,
        "9":34.2798125,
        "10":81.3601371,
        "11":115.3223611,
        "12":109.5987942}
segments = {
    "1": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[0:744],
    "2": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[744:1416],
    "3": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[1416:2160],
    "4": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[2160:2880],
    "5": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[2880:3624],
    "6": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[3624:4344],
    "7": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[4344:5088],
    "8": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[5088:5832],
    "9": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[5832:6552],
    "10": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[6552:7296],
    "11": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[7296:8016],
    "12": df["Preis (EUR/MWh, EUR/tCO2)"].iloc[8016:8760]}

for i in range(12):
        segments[f"{i+1}"]=(corr[f"{i+1}"]/segments[f"{i+1}"].mean())*segments[f"{i+1}"]

data = pd.concat(segments.values(), ignore_index=True)
data= data/1000
data.to_csv("data/grid_costs_2045.csv")
