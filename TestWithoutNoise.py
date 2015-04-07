# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 18:10:37 2013

@author: AZheltov
"""

import Signal
import Modulation

# Моделирование М-последовательностей

psi = Modulation.Modulation(128)
psi.M()

# Моделирование ситуации с 9ю целями

vim = [2000.0, 2000.0, 2030.0, 4000.0, 4000.0, 4030.0, 6000.0, 6000.0, 6030.0]
d = [50.0, 51.0, 51.0, 800.0, 801.0, 801.0, 3000.0, 3001.0, 3001.0]

sig = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 0.0, psi.psi, 'M9Targets')
sig.Generate()

sig.Doppler()

sig.todB()

sig.Surf()

sig.Image()

sig.PlotKD()
sig.PlotDF()