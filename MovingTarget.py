# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:22:26 2013

@author: AZheltov
"""

import numpy as np
import matplotlib.pyplot as plt

# движущийся имитатор
# параметры на Тп неизменны, изменяется скачкообразно
# без ускорения

def deg2rad(degrees):
    '''
    Функция перевода градусов в радианы
    '''
    radians = np.pi * degrees / 180.0
    return radians

def rad2deg(radians):
    '''
    Функция перевода радианов в градусы
    '''
    degrees = radians * 180.0 / np.pi
    return degrees

# D = 100.0
# beta = deg2rad(20.0)
V = -6000.0
psi = deg2rad(180.0)
f = 26.0
lam = 300.0 / f
Tp = 1.0

hi = psi

Tp = 6944 * 5 / 3 * 10**-6 # c

dl = V * Tp * 10**-3 # м

# Цикл по Тп

D = np.zeros(2*8192, dtype = float)
beta = np.zeros(2*8192, dtype = float)

D[0] = 4000.0
beta[0] = deg2rad(20.0)

for l in range(1,2*8192):
    D[l] = np.sqrt(D[l-1]*D[l-1] + dl*dl + 2.0 * D[l-1] * dl * np.cos(hi))
    dbeta = np.arcsin(dl * np.sin(hi) / D[l-1])
    VR = -V * np.cos(hi)
    hi += dbeta
    beta[l] = beta[l-1] + dbeta
    
plt.plot(D * np.cos(deg2rad(rad2deg(beta))), D * np.sin(deg2rad(rad2deg(beta))),'.-k')
plt.scatter(D[0] * np.cos(deg2rad(rad2deg(beta[0]))), D[0] * np.sin(deg2rad(rad2deg(beta[0]))),s=50, c='r')
plt.scatter(0, 0, s=100)
plt.grid(True)
plt.show()

# подсчет фаз