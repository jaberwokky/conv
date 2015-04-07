# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 10:43:29 2013

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

Ac = 8.0
dtau = 1.0
Ash = 20.0

Uc[n0:n0+Nzs] = Ac * values * np.exp(-i1 * 2.0 * pi * 0.0 *\
 np.arange(n0, n0+Nzs) * dtau * 10**-6)

Ac2 = 6.0
n02 = 36

Uc2 = np.zeros(Nd, dtype = np.complex64)

Uc2[n02:n02+Nzs] = Ac2 * values * np.exp(-i1 * 2.0 * pi * 0.0 *\
 np.arange(n02, n02+Nzs) * dtau * 10**-6)

hi = np.random.randn(Nd) + i1 * np.random.randn(Nd)

Uc += Uc2

tmp = Uc + Ash * np.array(hi)

B = 34
tmp[:B] = 0

tmpc = scipy.signal.fftconvolve(tmp, values.conjugate()[::-1], 'valid')[1:]

# tmp = 20.0 * np.log10(np.abs(tmp) / np.max(np.abs(tmp)))            

def signoise(sig):
    sig = np.abs(sig)
    sigmax = np.max(sig)
    sigarg = np.argmax(sig)
    
    sigcopy = np.array(sig)
    sigcopy[sigarg] = 0
    
    sigarg = np.argmax(sigcopy)
    
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

Uc2 = np.zeros(Nd, dtype = np.complex64)

Uc2[n02:n02+Nzs] = Ac2 * values2 * np.exp(-i1 * 2.0 * pi * 0.0 *\
 np.arange(n02, n02+Nzs) * dtau * 10**-6)

Uc += Uc2

hi = np.random.randn(Nd) + i1 * np.random.randn(Nd)

tmp2 = Uc + Ash * np.array(hi)

tmp2[:B] = 0

tmp2c = scipy.signal.fftconvolve(tmp2, values2.conjugate()[::-1], 'valid')[1:]

# tmp = 20.0 * np.log10(np.abs(tmp) / np.max(np.abs(tmp)))            

plotfig(tmp2c)

tmpall = tmpc + tmp2c

plotfig(tmpall)

# демодуляция

for n0 in [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44]: #in range(Nd-Nzs):

    tmpcret = np.array(tmp)

    tmpcret[n0:n0+Nzs] = tmpcret[n0:n0+Nzs] * values.conjugate()
    
    # модуляция комлиментарного кода
    
    tmpcret[n0:n0+Nzs] = tmpcret[n0:n0+Nzs] * values2
    
    tmpstrange = scipy.signal.fftconvolve(tmpcret, values2.conjugate()[::-1], 'valid')[1:]
    
    tmpafterstrange = tmpc + tmpstrange
    
    plotfig(tmpafterstrange)
    print(n0)