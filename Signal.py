# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 14:19:34 2013

@author: 1
"""

import Consts
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

class Signal:
    
    """ 
    Сигнал, отраженный от цели с заданными параметрами
    """
    
    def __init__(self, dtau, lambd, df, tp, vim, d, ac, ash, psi, name):
        self.dtau = dtau
        self.dd = self.dtau * 150.0
        self.nzs = 16384;
        self.tzs = self.Nzs * self.dtau
        self.tzskm = 0.15 * self.tzs
        self.tp = tp        
        self.nd = int(self.tp / self.dtau * 10**3)
        self.lambda_ = lambda_
        self.df = df
        self.ndvio = self.nd - self.nzs
        self.values = 1.0 * np.exp(Consts.I1 * psi)
        self.vim = vim
        self.d = d
        self.usigma = np.zeros(0, dtype=np.complex64)
        self.ac = ac
        self.ash = ash
        self.spectr = np.zeros(0, dtype=np.complex64)
        self.fmesh = np.arange(0.0, 71.0 * 10**3, self.df)
        self.u = np.zeros(0, dtype=np.complex64)
        self.df = 0.0
        self.kd = 0.0
        if isinstance(self.vim, list):
            self.numOfTargets = len(self.vim)
        else:
            self.numOfTargets = 1
            self.vim = list()
            self.d = list()
            self.vim.append(vim)
            self.d.append(d)
        self.d = np.array(self.d);
        self.f0 = 2.0 * np.array(self.vim) / self.lambda_
        self.name = list()
        self.maxA = list()
        self.maxAtest = list()
        self.maxDE = list()
        self.fullA = 0.0
        
        for i in range(self.NumOfTargets):
            self.name.append(name + 'V = ' + str(self.vim[i]) + ' ms, D = ' + \
                             str(self.d[i]) + ' km')

        for i in range(self.numOfTargets):
            self.name[i] = self.name[i].translate(None, '.')

    def __str__(self):
        
        return "OMG"
        
    def Generate(self):
        """
        Функция создания сигнала
        """

        tmp = np.zeros(self.nd, dtype=np.complex64)
        self.usigma = np.zeros(self.nd, dtype=np.complex64)
        for i in range(self.numOfTargets):   
            dnach = self.d[i] * 1000.0 #320000 # м
            dn = [n * self.dd for n in range(self.nd)]
            n0 = next(idx for idx, value in enumerate(dn) if value > dnach)
            uc = np.zeros(self.nd, dtype = np.complex64)
            n = np.arange(self.nd)
            uc[n0:n0+self.nzs] = self.ac * self.values * np.exp(-Consts.I1 * \
                                 2.0 * np.pi * self.f0[i] * np.arange(n0, n0+self.nzs) * \
                                 self.dtau * 10**-6)
            hi = np.random.randn(self.nd) + Consts.I1 * np.random.randn(self.nd)
            tmp = uc + self.ash * np.array(hi)
            self.usigma += tmp
            
        self.usigma[:self.nzs] = 0.0

    def Plot(self):
        """
        Вывести огибающую сигнала
        """
        
        plt.figure(figsize=(16,6))
        plt.plot(np.abs(self.usigma))
        plt.grid()
        plt.xlabel('Time, ms')
        plt.ylabel('Amplitude, dB')
        plt.xlim(0, self.nd)

    def Doppler(self):
        """
        Посчитать доплеровское смещение
        """

        self.u = np.zeros((self.ndvio, len(self.fmesh)), dtype=np.complex64)        
        
        t = 0
        for fn in self.fmesh:
            self.u[:, t] = scipy.signal.fftconvolve(self.usigma * np.exp(Consts.I1 * 2.0 * np.pi * \
                fn * self.dtau * 10**-6 * np.arange(self.nd)), self.values.conjugate()[::-1],   \
                'valid')[1:]
            t += 1

        self.kd = np.floor(self.d / 0.15)

        self.df = list()
        
        for i in range(self.numOfTargets):
            self.df.append(np.argwhere(self.fsetka == np.extract(np.array(self.f0[i])<=self.fmesh, self.fmesh)[0]))
        
        for i in range(self.numOfTargets):         
            self.df[i] = self.df[i].tolist()[0][0]
        
    def Fourier(self):
        """
        Посчитать дискретное преобразование Фурье
        """
        
        self.spectr = np.fft.fftshift(np.fft.fft(self.usigma))
        
    def Surf(self):
        """
        Вывести трехмерный график сигнала
        """

        for i in range(self.numOfTargets):
            fig = plt.figure(figsize = (16, 16))
            ax = fig.gca(projection = '3d')
    
            lftkd = self.Left(int(self.kd[i]-150))
            lftdf = self.Left(int(self.df[i]-150))
            
            rgtkd = int(self.kd[i]+150)
            rgtdf = int(self.df[i]+150)
            
            if (rgtkd - lftkd) != 300:
                rgtkd = 300 + lftkd
                
            if (rgtdf - lftdf) != 300:
                rgtdf = 300 + lftdf
            
            kd = np.arange(lftkd, rgtkd)
            df = np.arange(lftdf, rgtdf)
            
            x, y = np.meshgrid(kd, df)
                   
            ax.plot_surface(x, y, self.u[lftkd:rgtkd, lftdf:rgtdf], rstride=1, cstride=1, \
                            linewidth=0, cmap=cm.coolwarm, antialiased=True)    
        
            plt.title('Correlation Filter Field')    
            
            # plt.show()
        
            plt.xlabel('Range channels')
            plt.ylabel('Doppler channels')
            
            plt.grid(True)
            
            fig.savefig('Surf'+self.name[i]+'.png')
            
            plt.close(fig)
        
    def Left(self, value):
        """ 
        Левая граница
        """
        
        if (value <= 0):
            return 0
        else:
            return value
        
    def Contour(self):
        """
        Вывести на график контурные линии корреляцонно-фильтрового поля    
        """

        for i in range(self.NumOfTargets):
            
            fig = plt.figure(figsize = (16, 16))
    
            plt.contour(self.u[self.Left(int(self.kd[i]-150)):int(self.kd[i]+150), self.Left(int(self.df[i]-150)):int(self.df[i]+150)])
        
            plt.title('Correlation Filter Field')    
            
            # plt.show()
        
            plt.xlabel('Range channels')
            plt.ylabel('Doppler channels')
            
            fig.savefig('Contour'+self.name[i]+'.png')
            
            plt.close(fig)

    def Image(self):
        """
        Вывести на график корреляционно-фильтровое поле
        """

        for i in range(self.numOfTargets):

            fig = plt.figure(figsize = (16, 16))
    
            plt.imshow(self.u[self.Left(int(self.kd[i]-150)):int(self.kd[i]+150), self.Left(int(self.df[i]-150)):int(self.df[i]+150)])        
            
            plt.title('Correlation Filter Field')    
            
            # plt.show()
        
            plt.xlabel('Range channels')
            plt.ylabel('Doppler channels')
            
            fig.savefig('Image'+self.name[i]+'.png')
            
            plt.close(fig)
        
    def PlotKD(self):
        """
        Вывести на график распределение отсчетов сигнала по каналам дальности
        """
        for i in range(self.numOfTargets):            
            fig = plt.figure(figsize = (16, 6))
            plt.plot(self.u[:, self.df[i]])
            plt.grid(True)
            plt.xlabel('Range channels')
            plt.ylabel('Amplitude, dB')
    
            fig.savefig('PlotKD'+self.name[i]+'.png')
            
            plt.close(fig)    
    
    def PlotDF(self):        
        """
        Вывести на график распределение отсчетов сигнала по доплеровским фильтрам
        """

        for i in range(self.numOfTargets):            
            fig = plt.figure(figsize = (16, 6))
            plt.plot(self.u[self.kd[i], :])
            plt.grid(True)
            plt.xlabel('Doppler channels')
            plt.ylabel('Amplitude, dB')
    
            fig.savefig('PlotDF'+self.name[i]+'.png')
            
            plt.close(fig)        
        
    def todB(self):
        """
        Перевод в децибеллы
        """
        
        self.FullConv()
        self.u = 20.0 * np.log10(np.abs(self.u / self.fulla)
        
    def Amplitude(self):
        """ 
        Амплитуда сигнала
        """

        for i in range(self.numOfTargets):
            self.maxa.append(self.u[self.kd[i], self.df[i]])
        
        for i in range(self.numOfTargets):
            self.maxatest.append(np.max(self.u))
        
    def DopplerEffect(self):
        """
        Моделирование эффекта допплера        
        """

        v0d = np.argmax(self.u[:,0])
        
        for i in range(self.numOfTargets):        
            self.maxde.append((v0d, self.kd))

    def NoiseLevel(self):
        """
        
        """
        
    def FullConv(self):
        """
        Вычисление свертки сигнала        
        """

        dnach = 3000.0 * 1000.0 #320000 # м
        dn = [n * self.dd for n in range(self.nd)]
        n0 = next(idx for idx, value in enumerate(dn) if value > dnach)
        uc = np.zeros(self.nd, dtype=np.complex64)
        n = np.arange(self.nd)
        uc[n0:n0+self.Nzs] = self.ac * self.values * np.exp(-Consts.I1 * \
            2.0 * np.pi * 0.0 * np.arange(n0, n0+self.nzs) * self.dtau * \
            10**-6)
        hi = np.random.randn(self.nd) + Consts.I1 * np.random.randn(self.nd)
        tmp = uc + self.ash * np.array(hi)
        
        tmp = scipy.signal.fftconvolve(tmp, self.values.conjugate()[::-1],   \
            'valid')[1:]

        # tmp = 20.0 * np.log10(np.abs(tmp) / np.max(np.abs(tmp)))            

        self.fulla = np.max(np.abs(tmp))
