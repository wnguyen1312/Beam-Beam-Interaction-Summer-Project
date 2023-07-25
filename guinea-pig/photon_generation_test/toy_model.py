# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 21:07:34 2023

Toy model to compare WarpX and Guinea-Pig Photon-Generator

General idea: use the assumptions and parameters of Luca's file to put into
GP and use its method to generate photons.

Assumptions: 
    - Use the same number of macro-particles in both cases: 10k or 100k 
    - Monoenergetic beam: 125 GeV each
    - No time dependence
    - Find dz from GP - this is essentially the time interval
    - Find radius using the Lorentz equation (rmb relativistic correction)
    - Input into photon_generator function: upsilon calculated from the eq,
    eng = 125 GeV, dzOnRadius calculated.
    
@Author: William

"""
import numpy as np

#constants
c = 299792458 
e = 1.6e-19
m_e = 9.1093837*1e-31 #mass of electron in kg
m_e_keV = 511 #mass of electron in keV
h = 6.62607015e-34 #planck's constant
h_bar = h/(2*np.pi)
lambda_bar = h/(m_e*c) * 1/(2*np.pi) #reduced compton wavelength
GeV = 1e+9 * e


def find_gamma_electron(E): #energy in GeV
    gamma = E*1e+6 /m_e_keV
    return gamma
        
def find_speed_electron(E): #energy in GeV, speed in ms^-1
    gamma = find_gamma_electron(E)
    beta = np.sqrt(1-1/gamma**2)    
    return beta*c

def find_radius(E, B): #energy in GeV, B in Tesla, radius in m 
    m_e = 9.1093837*1e-31
    gamma = find_gamma_electron(E)
    v = find_speed_electron(E)
    return gamma*m_e*v/(e*B)

def get_upsilon_particle(E, B):
    radius = find_radius(E,B)
    gamma = find_gamma_electron(E)
    w_c = 3/2 * gamma*gamma*gamma * c /(radius)  #page 16 Daniel's thesis
    E = E * GeV #energy in J 
    upsilon = 2/3 * h_bar * w_c / E 
    return upsilon #good. matched with my previous estimate for pair calculation
    
def update_energy(E_photon): #update energy of emitting particle (e- or e+) based on energy of photon
#%% Set up parameters. Need to define energy, B and dz 

#Need a method to update the energy of the emitting particle
E = 125 
B = 1000
