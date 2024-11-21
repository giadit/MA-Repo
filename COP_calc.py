import pandas as pd
import numpy as np
from generate_demand import read_data

def eff_calc(T, TRY):
    df = read_data(TRY)
    df_temp = df["Temperature [°C]"]+273.15
    Tc = df_temp
    #COP = Th/(Th-Tc), eta = (Th-Tc)/Th
    #Tm = T2-T1/(ln(T2/T1))

    T1 = T- 55 + 273.15
    T2 = T + 273.15
    Tm = (T2-T1)/(np.log(T2/T1))
    COP_values = []
    eta_values = []
    for i in range(8760):
        COP_value = Tm/(Tm-Tc.iloc[i])
        COP_values.append(COP_value)

        eta_value = (Tm - Tc.iloc[i]) / Tm
        eta_values.append(eta_value)

    COP = pd.DataFrame(COP_values, columns=["COP"])
    eta = pd.DataFrame(eta_values, columns=["Efficiency"])

    if T == 150:
        corr = 0.1537 / eta.mean()
    else:
        corr = 0.1326 / eta.mean()
    COP = COP*0.45
    eta = eta*corr
    return COP, eta

if __name__ == "__main__":
    COP, eta = eff_calc(125, TRY=False)
    print(f"Roundtrip Efficiency: {float(COP.mean())*float(eta.mean())}")
    print(f"COP: {COP.mean()}, Eff. : {eta.mean()}")