# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 13:55:25 2023

@author: willi
"""
import read as rd

#for tesla design
energy = 500/2
sigma_x = 1000e-9
sigma_y = 100e-9
sigma_z = 2e-3
N = 4.2e+10
gamma = rd.find_gamma_electron(energy)
beamstrahlung = rd.find_beamstrahlung_average(N,
                                              gamma, sigma_x, sigma_y, sigma_z)