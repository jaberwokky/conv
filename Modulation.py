# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 16:05:45 2013

@author: 1
"""

import numpy as np
import Consts

class Modulation:
    """
    Модуляция сигнала
    """

    def __init__(self, Nkod):
        """
        Конструктор
        """
        self.nkod = nkod;
        self.psi = np.zeros(nkod, dtype=np.complex64)
        
    def m(self):
        """
        Модуляция с использованием М-последовательностей
        """
        f = open('mseq16k.out', 'r') # чтение из файла

        mseq = f.read()
        
        with open('mseq16k.out') as f:
            polyshape = []
            for line in f:
                line = line.split()  
                if line:            
                    line = int(line[0])
                    polyshape.append(line)
                    
        mseq = np.array(polyshape)
        self.psi = mseq * np.pi
    
    def lfm(self):
        """
        Линейно-частотная модуляция
        """
        
        fd = 1.0 * 10**6 # 1 МГц = 10^3 Гц
        fmin, fmax = -fd/2, fd/2
        f0 = (fmax + fmin) / 2
        tzs_sec = Consts.TZS / 1000000.0
        b = (fmax - fmin) / tzs_sec
        self.psi = 2.0 * np.pi * (f0 * (np.arange(Consts.NZS) * Consts.DTAU * 10**-6) + \
                   b/2.0 * (np.arange(Consts.NZS) * Consts.DTAU * 10**-6)**2)
        
    def hfm(self):
        """
        Гиперболически-частотная модуляция
        """
        i = np.arange(1, self.nkod**2+1)
        self.psi = np.pi * np.log(1.0 - 0.4 * (i-1)/(self.nkod**2)) / (0.2643/(self.nkod**2))
        
    def p4(self):
        """
        Модуляция с использованием модифицированных кодов Фрэнка
        """
        i = np.arange(self.nkod**2)
        self.psi = np.pi * (i) * (i-self.nkod**2) / self.nkod**2

    def frenk(self):
        """
        Модуляция с использованием кодов Фрэнка
        """
        i = np.arange(self.nkod)
        j = np.arange(self.nkod)
        self.psi = 2.0*np.pi / self.nkod*np.outer(i,j) 
        self.psi = self.psi.flatten()

    def complim(self):
        """
        Модуляция с использованием комплиментарных кодов
        """
        i = np.arange(self.nkod**2)
        self.psi = np.zeros(self.nkod**2)
