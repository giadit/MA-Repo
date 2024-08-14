import datetime
import os

import numpy as np
import pandas as pd

import demandlib.bdew as bdew
import matplotlib.pyplot as plt
def gen_heat_demand(df_temp):

    #anzahl_MFH = 35 # 15 WE pro MFH = 525 WE
    #beh_wohnfl_proMFH = 1091.9 # m2
    #heizbed_pro_mq = 133 # kWh/m2a

    # define holidays for Berlin for 2023
    holidays = {
        datetime.date(2023, 1, 1): "New year",
        datetime.date(2023, 3, 8): "Frauentag",
        datetime.date(2023, 4, 7): "Karfreitag",
        datetime.date(2023, 4, 10): "Easter Monday",
        datetime.date(2023, 5, 1): "Labour Day",
        datetime.date(2023, 5, 18): "Himmelfahrt",
        datetime.date(2023, 5, 29): "Pfingstmontag",
        datetime.date(2023, 10, 3): "Day of German Unity",
        datetime.date(2023, 12, 25): "Christmas Day",
        datetime.date(2023, 12, 26): "Second Christmas Day",
    }
    #create DataFrame for demand
    demand = pd.DataFrame(index=pd.date_range(datetime.datetime(
        2023, 1, 1, 0), periods=8760, freq="h"))

    #Generate demand for building types
    demand["mfh"] = bdew.HeatBuilding(
        demand.index,
        holidays=holidays,
        temperature=df_temp,
        shlp_type="MFH",
        building_class=3,
        wind_class=0,
        annual_heat_demand=5082794.5, # kWh/a
        name="MFH",
    ).get_bdew_profile()

    # Plot demand of building
    ax = demand.plot()
    ax.set_xlabel("Date")
    ax.set_ylabel("Heat demand in kW")
    plt.show()
    #Save Plot
    plt.savefig("results/demand_data.png", dpi=300)
    return demand