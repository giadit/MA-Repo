import pvlib

from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS


import matplotlib.pyplot as plt
import pandas as pd

def fetch_pv_data():
    location = Location(latitude=52.500,
                        longitude=12.285,tz="Europe/Berlin",
                        altitude=14.5,name="Berlin avg.")

    df_pv = pd.read_csv("data/pvlib_berlin_2023.csv", index_col=0)
    df_pv.index = pd.to_datetime(df_pv.index)

   #cec_modules = pvlib.pvsystem.retrieve_sam("cecmod")
   #cec_inverters = pvlib.pvsystem.retrieve_sam("CECInverter")

   #module = cec_modules["SunPower_SPR_400E_WHT_D"]
   #print(module)
   #inverter = cec_inverters["ABB__PVI_CENTRAL_250_US__480V_"]
   #print(inverter)
    module = {
        'Name': 'SunPower Maxeon 3 400 W',
        'pdc0': 400,  # Nominal max power (W)
        'gamma_pdc': -0.0027,  # Power temperature coefficient (%/°C)
        'efficiency': 0.226  # Module efficiency
    }

    # Inverter (SMA Sunny Tripower 25000TL) parameters
    inverter = {
        'pdc0': 25000,  # Max AC power output (W)
        'eta_inv_nom': 0.981  # Inverter efficiency
    }

    temperature_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]

    system_east = PVSystem(
        surface_tilt=27,  # Tilt angle of the roof
        surface_azimuth=90,  # East-facing roof
        module_parameters=module,
        inverter_parameters=inverter,
        temperature_model_parameters= temperature_parameters,
        modules_per_string=28,  # 28 panels per string / 199.5*0.5/1.72 = 56
        strings_per_inverter=2  #  2 strings for this inverter configuration
    )
    system_west = PVSystem(
        surface_tilt=27,  # Tilt angle of the roof
        surface_azimuth=270,  # West-facing roof
        module_parameters=module,
        inverter_parameters=inverter,
        temperature_model_parameters=temperature_parameters,
        modules_per_string=28,  # Same configuration as the East-facing system
        strings_per_inverter=2
    )

    mc_east = ModelChain(system_east, location, aoi_model="ashrae", spectral_model="no_loss")
    mc_west = ModelChain(system_west, location, aoi_model="ashrae", spectral_model="no_loss")

    mc_east.run_model(df_pv)
    mc_west.run_model(df_pv)

    # Get AC power output
    #scaled for 35 units
    #scaled to kW
    power_east = 35*mc_east.results.ac/1000
    power_west = 35*mc_west.results.ac/1000

    # Combine both systems' outputs
    total_power = power_east + power_west
    total_power= total_power.to_frame()
    # Plot total power output
    #total_power.plot(label='Total Power (East + West)', color='blue')
    #power_east.plot(label='East Power', color='orange')
    #plt.figure(figsize=(10, 6))
    #power_west.plot(label='West Power', color='green')
    #plt.ylabel('AC Power Output (kW)')
    #plt.legend()
    #plt.show()

    #system = PVSystem(surface_tilt=45,surface_azimuth=180,
    #                  module_parameters=module, inverter_parameters=inverter,
    #                  temperature_model_parameters=temperature_parameters,
    #                  modules_per_string=7, strings_per_inverter=2)
    #
    #modelchain = ModelChain(system,location)
    #
    #pv_data = modelchain.run_model(df_pv)
    #pv_data.results.ac.plot(figsize=(16,9))
    ##modelchain.results.ac.resample("M").sum().plot(figsize=(16,9))
    #plt.show()
    return total_power

if __name__ == "__main__":
    pv_data = fetch_pv_data()
    pv_data.to_csv("results/pv_data_results.csv")
    print(pv_data)