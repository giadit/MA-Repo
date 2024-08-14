# -*- coding: utf-8 -*-
"""
Created on Sun May 12 11:45:50 2024

@author: gadit
"""
import matplotlib.pyplot as plt
import pandas as pd

import oemof.solph as solph
from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components as cmp
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import helpers
from oemof.solph import processing
from oemof.solph import views

data = pd.read_csv("basic_example.csv")

year_index = create_time_index(year=2022, number=len(data))
energysys = solph.EnergySystem(timeindex=year_index, infer_last_interval=False)


bgas = buses.Bus(label="natural gas")
bel = buses.Bus(label="electricity")
energysys.add(bgas,bel)

#excess component for overproduction of el
energysys.add(
    cmp.Sink(
        label="excess_bel", 
        inputs={bel: flows.Flow()}))
#create gas source
energysys.add(
    cmp.Source(
        label="rgas",
        outputs={bgas: flows.Flow()}))
#fixed source for wind
energysys.add(
    cmp.Source(
        label="wind",
        outputs={bel: flows.Flow(fix=data["wind"], nominal_value=1000000)}))
#fixed source for pv
energysys.add(
    cmp.Source(
        label="pv",
        outputs={bel: flows.Flow(fix=data["pv"], nominal_value=582000)}))
#adding demand
energysys.add(
        cmp.Sink(
        label="demand_el", 
        inputs={bel: flows.Flow(fix= data["demand_el"], nominal_value = 1)}))
#create convereter for power plant
energysys.add(cmp.Converter(
        label = "pp_gas",
        inputs={bgas: flows.Flow()},
        outputs={bel: flows.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58}))
#create storage system
energysys.add(cmp.GenericStorage(
        nominal_storage_capacity=10077997,
        label = "storage",
        inputs = {bel: flows.Flow(nominal_value=1007797/6)},
        outputs = {bel: flows.Flow(nominal_value=1007797/6, variable_costs=0.001)},
        loss_rate = 0.00,
        initial_storage_level = None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8))

"create optimization"
om = solph.Model(energysys)
om.solve(solver='cbc', solve_kwargs={'tee': True})
om.write('my_model.lp', io_options={'symbolic_solver_labels': True})
energysys.results = processing.results(om)
results = solph.processing.results(om)

node_wind = energysys.groups['wind']
print(results[(node_wind, bel)])

