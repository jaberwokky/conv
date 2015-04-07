# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 18:48:55 2013

@author: AZheltov
"""

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

plt.close('all')

pi = np.pi

code1 = np.array([0,0,0,pi,0,0,pi,0,0 ,0 ,0 ,pi,pi,pi,0 ,pi])
code2 = np.array([0,0,0,pi,0,0,pi,0,pi,pi,pi,0 ,0 ,0 ,pi,0])
#code2 = np.abs(code1 - pi)

i1 = np.complex(0.0,1.0)

values = np.exp(i1 * code1)
values2 = np.exp(i1 * code2)

Nd = 16*2 + 40

Uc = np.zeros(Nd, dtype = np.complex64)

n = np.arange(Nd)

Nzs = 16

n0 = 24

Ac = 10.0
dtau = 1.0
Ash = 0.0

Uc[n0:n0+Nzs] = Ac * values * np.exp(-i1 * 2.0 * pi * 0.0 *\
 np.arange(n0, n0+Nzs) * dtau * 10**-6)

hi = np.random.randn(Nd) + i1 * np.random.randn(Nd)

tmp = Uc + Ash * np.array(hi)

tmpc = scipy.signal.fftconvolve(tmp, values.conjugate()[::-1], 'valid')[1:]

# tmp = 20.0 * np.log10(np.abs(tmp) / np.max(np.abs(tmp)))            

def signoise(sig):
    sig = np.abs(sig)
    sigmax = np.max(sig)
    sigarg = np.argmax(sig)
    
    sigcopy = np.array(sig)
    sigcopy[sigarg] = 0
    sigmaxnoise = np.max(sigcopy)
    
    print(sigmax - sigmaxnoise)
    
    return (sigmax - sigmaxnoise)

def plotfig(sig):
    plt.figure()
    plt.plot(np.abs(sig))
    plt.grid(True)
    
    sgn = signoise(sig)
    
    plt.text(30,100, sgn)

plotfig(tmpc)

Uc[n0:n0+Nzs] = Ac * values2 * np.exp(-i1 * 2.0 * pi * 0.0 *\
 np.arange(n0, n0+Nzs) * dtau * 10**-6)

hi = np.random.randn(Nd) + i1 * np.random.randn(Nd)

tmp2 = Uc + Ash * np.array(hi)

tmp2c = scipy.signal.fftconvolve(tmp2, values2.conjugate()[::-1], 'valid')[1:]

# tmp = 20.0 * np.log10(np.abs(tmp) / np.max(np.abs(tmp)))            

plotfig(tmp2c)

tmpall = tmpc + tmp2c

plotfig(tmpall)

# демодуляция

tmpcret = tmp

tmpcret[n0:n0+Nzs] = tmpcret[n0:n0+Nzs] * values.conjugate()

# модуляция комлиментарного кода

tmpcret[n0:n0+Nzs] = tmpcret[n0:n0+Nzs] * values2

tmpstrange = scipy.signal.fftconvolve(tmpcret, values2.conjugate()[::-1], 'valid')[1:]

tmpafterstrange = tmpc + tmpstrange

plotfig(tmpafterstrange)