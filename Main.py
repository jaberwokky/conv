# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 14:19:08 2013

@author: 1
"""

import Signal
import Modulation

# Моделирование М-последовательностей

psi = Modulation.Modulation(128)
psi.M()

# Моделирование ситуации с 9ю целями

vim = [2000.0, 2000.0, 2030.0, 4000.0, 4000.0, 4030.0, 6000.0, 6000.0, 6030.0]
d = [50.0, 51.0, 51.0, 800.0, 801.0, 801.0, 3000.0, 3001.0, 3001.0]

sig = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M9Targets')
sig.Generate()

sig.Doppler()

sig.todB()

sig.Surf()

sig.Image()

sig.PlotKD()
sig.PlotDF()

# Одна цель, изменение скорости

vim = 0.0
d = 3001.0

sig1 = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig1.Generate()

sig1.Doppler()

sig1.todB()

sig1.Surf()

sig1.Image()

sig1.PlotKD()
sig1.PlotDF()

sig1.DopplerEffect()
sig1.Amplitude()

# Одна цель, изменение скорости

vim = 2000.0
d = 3001.0

sig2 = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig2.Generate()

sig2.Doppler()

sig2.todB()

sig2.Surf()

sig2.Image()

sig2.PlotKD()
sig2.PlotDF()

sig2.DopplerEffect()
sig2.Amplitude()

# Одна цель, изменение скорости

vim = 4000.0
d = 3001.0

sig3 = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig3.Generate()

sig3.Doppler()

sig3.todB()

sig3.Surf()

sig3.Image()

sig3.PlotKD()
sig3.PlotDF()

sig3.DopplerEffect()
sig3.Amplitude()

# Одна цель, изменение дальности

vim = 4000.0
d = 50.0

sig1d = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig1d.Generate()

sig1d.Doppler()

sig1d.todB()

sig1d.Surf()

sig1d.Image()

sig1d.PlotKD()
sig1d.PlotDF()

sig1d.DopplerEffect()
sig1d.Amplitude()

# Одна цель, изменение дальности

vim = 4000.0
d = 800.0

sig2d = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig2d.Generate()

sig2d.Doppler()

sig2d.todB()

sig2d.Surf()

sig2d.Image()

sig2d.PlotKD()
sig2d.PlotDF()

sig2d.DopplerEffect()
sig2d.Amplitude()

# Одна цель, изменение дальности

vim = 4000.0
d = 3000.0

sig3d = Signal.Signal(1.0, 0.23, 60.0, 40.0, vim, d, 10.0, 1.0, psi.psi, 'M1Target')
sig3d.Generate()

sig3d.Doppler()

sig3d.todB()

sig3d.Surf()

sig3d.Image()

sig3d.PlotKD()
sig3d.PlotDF()

sig3d.DopplerEffect()
sig3d.Amplitude()