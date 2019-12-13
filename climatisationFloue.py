# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 19:13:52 2019

@author: Nicolas
"""


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

temperature = ctrl.Antecedent(np.arange(5, 65, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(16, 100, 1), 'humidity')
power = ctrl.Consequent(np.arange(0.0, 3.0, 0.01), 'power')

temperature.automf(7)
humidity.automf(7)

temperature['VVC'] = fuzz.trimf(temperature.universe, [5, 5, 15])
temperature['VC'] = fuzz.trimf(temperature.universe, [5, 15, 25])
temperature['C'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['F'] = fuzz.trimf(temperature.universe, [25, 35, 45])

humidity['VVL'] = fuzz.trimf(humidity.universe, [16, 16, 30])
humidity['VL'] = fuzz.trimf(humidity.universe, [16, 30, 44])
humidity['L'] = fuzz.trimf(humidity.universe, [30, 44, 58])
humidity['M'] = fuzz.trimf(humidity.universe, [44, 58, 72])

power['VVL'] = fuzz.trapmf(power.universe, [0, 0, 0.166, 0.333])
power['VL'] = fuzz.trapmf(power.universe, [0.166, 0.333, 0.666, 0.833])
power['L'] = fuzz.trapmf(power.universe, [0.666, 0.833, 1.166, 1.333])
power['M'] = fuzz.trapmf(power.universe, [1.166, 1.333, 1.666, 1.833])
power['H'] = fuzz.trapmf(power.universe, [1.666, 1.833, 2.166, 2.333])
power['VH'] = fuzz.trapmf(power.universe, [2.166, 2.333, 2.666, 2.833])

rule1 = ctrl.Rule(temperature['VVC'] | humidity['VVL'], power['VVL'])
rule2 = ctrl.Rule(temperature['VVC'] | humidity['VL'], power['VVL'])
rule3 = ctrl.Rule(temperature['VVC'] | humidity['L'], power['VL'])
rule4 = ctrl.Rule(temperature['VVC'] | humidity['M'], power['VL'])
rule5 = ctrl.Rule(temperature['VC'] | humidity['VVL'], power['VVL'])
rule6 = ctrl.Rule(temperature['VC'] | humidity['VL'], power['VL'])
rule7 = ctrl.Rule(temperature['VC'] | humidity['L'], power['VL'])
rule8 = ctrl.Rule(temperature['VC'] | humidity['M'], power['L'])
rule9 = ctrl.Rule(temperature['C'] | humidity['VVL'], power['VL'])
rule10 = ctrl.Rule(temperature['C'] | humidity['VL'], power['VL'])
rule11 = ctrl.Rule(temperature['C'] | humidity['L'], power['L'])
rule12 = ctrl.Rule(temperature['C'] | humidity['M'], power['L'])
rule13 = ctrl.Rule(temperature['F'] | humidity['VVL'], power['VL'])
rule14 = ctrl.Rule(temperature['F'] | humidity['VL'], power['L'])
rule15 = ctrl.Rule(temperature['F'] | humidity['L'], power['L'])
rule16 = ctrl.Rule(temperature['F'] | humidity['M'], power['M'])

power_ctrl = ctrl.ControlSystem([rule1,rule1, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16])
power_calcul = ctrl.ControlSystemSimulation(power_ctrl)

power_calcul.input['temperature'] = 35
power_calcul.input['humidity'] = 100

power_calcul.compute()

print(power_calcul.output['power'])
power.view(sim=power_calcul)