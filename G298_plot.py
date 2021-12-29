#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

import mu_vs_mu

bulk = {'Energy' : -1752.1542, 'F-Units' : 12.0}

#Zn_rich
H2O_4_nHmim_2 = {'M': 24, 'X': -4, 'Y': 8, 'Area': 825.64, 'Energy': -3308.28,   'Label': '4 Water - 2 Hmim'}
H2O_3_nHmim_2 = {'M': 24, 'X': -4, 'Y': 6, 'Area': 825.64, 'Energy': -3279.64,   'Label': '3 Water - 2 Hmim'}
H2O_2_nHmim_2 = {'M': 24, 'X': -4, 'Y': 4, 'Area': 825.64, 'Energy': -3251.01,   'Label': '2 Water - 2 Hmim'}

H2O_3_nHmim =   {'M': 24, 'X': -2, 'Y': 6, 'Area': 825.64, 'Energy': -3427.14,   'Label': '3 Water - 1 Hmim'}
H2O_2_nHmim =   {'M': 24, 'X': -2, 'Y': 4, 'Area': 825.64, 'Energy': -3398.58,   'Label': '2 Water - 1 Hmim'}
H2O_nHmim =     {'M': 24, 'X': -2, 'Y': 2, 'Area': 825.64, 'Energy': -3369.25,   'Label': '1 Water - 1 Hmim'}

#ZnL2
H2O_2 =         {'M': 24, 'X':  0, 'Y': 4, 'Area': 825.64, 'Energy': -3546.05,   'Label': '2 Water'}
H2O =           {'M': 24, 'X':  0, 'Y': 2, 'Area': 825.64, 'Energy': -3517.42,   'Label': '1 Water'}
Stoich =        {'M': 24, 'X':  0, 'Y': 0, 'Area': 825.64, 'Energy': -3487.47,   'Label': 'Stoich Zn(mim)$_2$'}

#L_rich
H2O_Hmim =      {'M': 24, 'X':  2, 'Y': 2, 'Area': 825.64, 'Energy': -3664.73,   'Label': '1 Water + 1 Hmim'}
Hmim =          {'M': 24, 'X':  2, 'Y': 0, 'Area': 825.64, 'Energy': -3635.69,   'Label': '1 Hmim'}
Hmim_2 =        {'M': 24, 'X':  4, 'Y': 0, 'Area': 825.64, 'Energy': -3783.79,   'Label': '2 Hmim'}

#data = [H2O_2, H2O, Stoich, Hmim, H2O_Hmim, Hmim_2, H2O_nHmim, H2O_2_nHmim, H2O_3_nHmim, H2O_4_nHmim_2, H2O_3_nHmim_2, H2O_2_nHmim_2] 
data = [H2O_4_nHmim_2, H2O_3_nHmim_2, H2O_2_nHmim_2, H2O_3_nHmim, H2O_2_nHmim, H2O_nHmim, H2O_2, H2O, Stoich, H2O_Hmim, Hmim, Hmim_2]

deltaX = {'Range': [ -75.124, -72.124],  'Label': 'Hmim'}
deltaY = {'Range': [ -16.659, -13.659], 'Label': 'H_2O'}

X_0 = -72.864
Y_0 = -14.084

mu_vs_mu.calculate(data, bulk, deltaX, deltaY, X_0, Y_0,temperature=298, convert_pressure=True)

