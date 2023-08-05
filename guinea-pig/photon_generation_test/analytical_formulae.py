# -*- coding: utf-8 -*-
"""

Testing agreement of analytical formulae at low energies: 
    - Ternov and Solokov (quantum)
    - Jackson (classical)

Pre-factors are set to 1 

Created on Fri Aug  4 10:40:28 2023

@author: william nguyen

"""

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.constants import c, e as q_e, m_e, alpha, hbar, eV, pi, epsilon_0, physical_constants
from scipy.integrate import odeint, quad, nquad, quad_vec, dblquad 
from scipy.special import kv

#CONSTANTS
GeV = 1e9*eV 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
r_e = physical_constants['classical electron radius'][0]
E_S = m_e**2 * c**3 / (q_e * hbar) 


#PARAMETERS

energy = 125.*GeV
energy_GeV = energy / GeV
gamma = energy / (m_e*c**2) + 1. 
pz = np.sqrt(gamma**2-1)*m_e*c;
vz = pz / (m_e*gamma) 
B = 1e3 
rho = gamma*m_e*vz/(q_e*B)


#%% JACKSON formula (14.93) 
I = q_e**2*gamma**4/(3.*rho)/epsilon_0
omega_c = 3./2. * gamma**3 * c/rho
E_c = omega_c * hbar 

omega = np.linspace(1e-5*omega_c, 10*omega_c, 2000)

omega = omega_c * np.logspace(-5,1,2000)

E = omega*hbar/GeV

def y(omega):
    return omega/ omega_c
    
def integrand(x):
    return I/(hbar*omega_c)*kv( 5./3., x)

dN_dy = []
for w in omega:
    val, err = quad(integrand, y(w), np.inf)
    dN_dy = np.append(dN_dy, val)

dN_dE = dN_dy/E_c
N = np.trapz(dN_dE, E) 
dE = E[1]-E[0]

classical_energy = E
classical_spectra = dN_dE/N

del E, N, dN_dE 


#QUANTUM FORMULA 

u_c = omega_c * hbar #same as E_c
E = energy #energy of the beam/emmiting particle 
P_c = 2./3. *r_e * m_e*c**2 *gamma**4 / (rho**2) #total radiation power
xi = u_c / E #quantum correction parameter


#u = np.linspace(1e-4*GeV, 0.8*energy, 2000) #SI unit 

u = GeV * np.logspace(-4,2,2000)
factor = 2*pi*rho/c * 1/u #conversation factor to go from power --> intensity --> number spectra


def y_quantum(u): #u = energy of photon
    return u/u_c * 1/(1-u/E) 
    
def integrand(x): #this is integrand part of F(y, xi) in equation 28
    return kv( 5./3., x)

F = []
for photon_energy in u:
    y = y_quantum(photon_energy) #same notation as the Japanese paper
    val, err = quad(integrand, y, np.inf)
    outside_term = y/(1+xi*y)**3
    second_term =  xi**2 * y**2 /(1+xi*y) * kv( 2./3., y) #the term without the integral
    F_value = outside_term*(val + second_term)
    F.append(F_value)

F = np.array(F)
dP_du = P_c * (1+xi*y)**2 /u_c * F # dP/dE
dN_du = dP_du *factor

N = np.trapz(dN_du, u/GeV) 

quantum_energy = u/GeV
quantum_spectra = dN_du/N

#%%Plotting. Classical --> quantum in low energies 

plt.plot(classical_energy, classical_energy*classical_spectra, label='classical formula')
plt.plot(quantum_energy, quantum_energy*quantum_spectra, label='quantum formula')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Energy [GeV]', font=14)
plt.ylabel('E/N dN/dE [1/GeV]', font=14)
plt.tight_layout()
plt.show()

#%%Plotting. Classical --> quantum in low energies 

plt.plot(classical_energy, quantum_spectra/classical_spectra)
plt.legend()
plt.xscale('log')
plt.xlabel('Energy [GeV]', font=14)
plt.ylabel('Ratio', font=14)
plt.tight_layout()
plt.show()

