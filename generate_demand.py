import datetime
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import demandlib.bdew as bdew
import demandlib.particular_profiles as profiles


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

def gen_heat_demand(df_temp):

    #anzahl_MFH = 35 # 15 WE pro MFH = 525 WE
    #beh_wohnfl_proMFH = 1091.9 # m2
    #heizbed_pro_mq = 133 # kWh/m2a
    annual_heat_demand = {"MFH" : 5082794.5}

    # 2890  el kWh je Haushalt (2 Personen) 2890*525 = 1517250
    annual_el_demand = {"h0_dyn" : 1517250}


    # define holidays for Berlin for 2023
    year = 2023

    holidays = {
        datetime.date(year, 1, 1): "New year",
        datetime.date(year, 3, 8): "Frauentag",
        datetime.date(year, 4, 7): "Karfreitag",
        datetime.date(year, 4, 10): "Easter Monday",
        datetime.date(year, 5, 1): "Labour Day",
        datetime.date(year, 5, 18): "Himmelfahrt",
        datetime.date(year, 5, 29): "Pfingstmontag",
        datetime.date(year, 10, 3): "Day of German Unity",
        datetime.date(year, 12, 25): "Christmas Day",
        datetime.date(year, 12, 26): "Second Christmas Day",
    }


    #create DataFrame for demand
    demand = pd.DataFrame(index=pd.date_range(datetime.datetime(
        year, 1, 1, 0), periods=8760, freq="h"))

    #Generate demand for building types
    demand["MFH"] = bdew.HeatBuilding(
        demand.index,
        holidays=holidays,
        temperature=df_temp,
        shlp_type="MFH",
        building_class=3,
        wind_class=0,
        annual_heat_demand=annual_heat_demand["MFH"], # kWh/a
        name="mfh",
    ).get_bdew_profile()

    # read standard load profiles
    e_slp = bdew.ElecSlp(year, holidays=holidays)

    # multiply given annual demand with timeseries
    elec_demand = e_slp.get_profile(annual_el_demand)

    # Resample 15-minute values to hourly values.
    elec_demand_resampled = elec_demand.resample("h").mean()
    print(elec_demand_resampled.sum())
    demand["demand_el"] = elec_demand_resampled

   ## Plot demand of building
   #ax = demand["MFH"].plot()
   #ax.set_ylabel("Heat demand in kW")
   #plt.savefig("results/heat_demand_data.png",dpi=1200)
   #plt.show()
   #
   #plt.clf()
   #
   ## Plot demand
   #ax = elec_demand_resampled.plot()
   #ax.set_ylabel("Power demand")
   #plt.savefig("results/el_demand_data.png",dpi=1200)
   #plt.show()

    return demand

df = read_data(TRY=True)
df_temp = df["Temperature [°C]"]
demand = gen_heat_demand(df_temp)
print(demand["demand_el"])