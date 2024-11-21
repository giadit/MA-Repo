import pandas as pd
import numpy as np
from generate_demand import read_data

def eff_calc(T, norm):
    df = read_data(TRY=False)
    df_temp = df["Temperature [°C]"]+273.15
    Tc = df_temp + 5
    #COP = Th/(Th-Tc), eta = (Th-Tc)/Th
    #Tm = T2-T1/(ln(T2/T1))
    if norm == True:
        COP_values = []
        eta_values = []

        T1 = 155 - 55 + 273.15
        T2 = 155 + 273.15
        T1e = 145 -55 +273.15
        T2e = 145 +273.15
        Tm = (T2-T1)/(np.log(T2/T1))
        Tme = (T2e-T1e)/(np.log(T2e/T1e))
        for i in range(8760):
            COP_value = Tm/(Tm-Tc.iloc[i])
            COP_values.append(COP_value)

            eta_value = (Tme - Tc.iloc[i]) / Tme
            eta_values.append(eta_value)

        COP = pd.DataFrame(COP_values, columns=["COP"])
        eta = pd.DataFrame(eta_values, columns=["Efficiency"])
        correction = float(3.21375/COP.mean())
        corr = 0.15/eta.mean()

    T1 = T + 5 - 55 + 273.15
    T2 = T + 5 + 273.15
    T1e = T -5 - 55 + 273.15
    T2e = T -5 + 273.15
    Tm = (T2-T1)/(np.log(T2/T1))
    Tme = (T2e - T1e) / (np.log(T2e / T1e))
    COP_values = []
    eta_values = []
    for i in range(8760):
        COP_value = Tm/(Tm-Tc.iloc[i])
        COP_values.append(COP_value)

        eta_value = (Tme - Tc.iloc[i]) / Tme
        eta_values.append(eta_value)

    COP = pd.DataFrame(COP_values, columns=["COP"])
    eta = pd.DataFrame(eta_values, columns=["Efficiency"])
    if norm == True:
        COP = COP*correction
        eta = eta*corr
    return COP, eta

if __name__ == "__main__":
    COP, eta = eff_calc(125, norm=True)
    print(f"Roundtrip Efficiency: {float(COP.mean())*float(eta.mean())}")
    print(f"COP: {COP.mean()}, Eff. : {eta.mean()}")