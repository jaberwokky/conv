# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 16:25:47 2013

@author: 1
"""

class Radar:
    def __init__(self):
        self.dtau = 1.0;
        self.lambd = 0.23;
        self.df = 60.0;
        self.Tp = 40.0;
        self.dD = self.dtau * 150.0