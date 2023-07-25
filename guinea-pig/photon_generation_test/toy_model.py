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
import math 
import random
#constants
c = 299792458 
e = 1.6e-19
m_e = 9.1093837*1e-31 #mass of electron in kg
m_e_keV = 511 #mass of electron in keV
h = 6.62607015e-34 #planck's constant
h_bar = h/(2*np.pi)
lambda_bar = h/(m_e*c) * 1/(2*np.pi) #reduced compton wavelength
GeV = 1e+9 * e
EMASS = (0.51099906/1000) #mass of electron in GeV


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
    


def synradKi53andK23(x):
    "Function to approximate modified bessel functions"
    if x <= 1.54:
        x1 = x ** 0.6666666667
        x2 = x1 * x1
        x1inv = 1.0 / x1
        Ki53 = ((0.03363782042 * x1 - 0.1134842702) * x2 + 0.3944669710) * x2 - 1.812672515 + 2.1495282415344901 * x1inv
        K23 = (((0.04122878139 * x1 - 0.1494040962) * x2 + 0.7862616059) * x1 - 1.258219373) * x1 + 1.074647298 * x1inv
    elif x <= 4.48:
        Ki53 = ((0.09120815010 * x - 1.229105693) * x + 4.442223505) / (((x - 0.6903991322) * x + 5.651947051) * x - 0.9691386396)
        K23 = ((0.08194471311 * x - 1.112728296) * x + 4.052334415) / (((x - 0.6524469236) * x + 6.1800441958) * x - 0.4915880600)
    elif x <= 165.0:
        c = math.exp(-x) / math.sqrt(x)
        Ki53 = c * (2.187014852 + 1.253535946 * x) / (0.9949036186 + x)
        K23 = c * (0.6120387636 + 1.253322122 * x) / (0.3915531539 + x)
    else:
        Ki53 = 0.0
        K23 = 0.0

    return Ki53, K23


def synrad_0_no_spin_flip(upsilonSingleP, eng, dzOnRadius):
    #x = 0.0
    #p0, p1, v1, v3, g = 0.0, 0.0, 0.0, 0.0, 0.0
    #fKi53, fK23 = 0.0, 0.0

    if eng <= 0.0:
        print("Initial particle energy below zero:", eng)
        return 1, 0.0  # Return both flag and photon energy as a tuple

    upsilon = float(upsilonSingleP)
    upsilon_bar = 1.5 * upsilon
    gamma = eng / EMASS  # Energy divided by mass of electron (in GeV)
    factor = (1.0 + 0.5 * upsilon_bar)**(1/3)
    p0 = 1.297210720417891e-02 * dzOnRadius * gamma / factor #dt: time interval = dz in GP 

    rndm_generator = random.random()  # This is p in the Japanese paper

    if rndm_generator > p0: #p vs p_0
        return 0, 0.0

    p1 = random.random()
    while True:
        v1 = random.random()
        if v1 != 0.0:
            break

    v3 = v1 * v1 * v1
    xden = 1.0 - v3 + 0.5 * upsilon_bar * (1.0 + v3 * v3)
    x = upsilon_bar * v3 / xden
    x1 = 1.0 - x
    z = x / (upsilon_bar * x1)
    fKi53, fK23 = synradKi53andK23(z)
    F00 = fKi53 + (x * x / x1) * fK23

    dxdy = 3.0 * v1 * v1 * (upsilon_bar + x * (1.0 - upsilon_bar * v3)) / xden
    g = F00 * dxdy * factor / (9.67287708690521 * upsilon)

    if p1 < g:
        photonEnergy = eng * x #formula 47
        return 1, photonEnergy
    else:
        photonEnergy = 0.0
        return 0, photonEnergy
    

    
#this function can be useful if we want to update the emitting particle energy
#for when we go into cases where we want timesteps or evolution? 
def initialize_beam_particles(energy, num_macro_particles, B, dz):
    """
    Initialize beam particles with a given energy and additional properties.

    Parameters:
        energy (float): Energy of each particle in GeV.
        num_macro_particles (int): Number of macro-particles to be initialized.
        B (float): Magnetic field strength in Tesla (required for calculating radius).
        dzOnRadius (float): Ratio of dz to radius (required for particle movement).

    Returns:
        list: A list of dictionaries, where each dictionary represents a beam particle with its properties.
    """
    beam_particles = []
    for _ in range(num_macro_particles):
        particle = {
            "energy": energy,
            "radius": find_radius(energy, B),  # Calculate initial radius
            "dz": dz,  # Initial dz (time interval) as a fraction of radius
            "upsilon": get_upsilon_particle(energy, B)  # Calculate initial upsilon
        }
        beam_particles.append(particle)
    return beam_particles



#%% Start the photon generation proccess 

import photon_generator

dz = 1e-6 #not sure yet
eng = 125 #125 GeV each beam. Mono-energetic 
B = 1e+3 #around 1000 T
upsilonSingleP = get_upsilon_particle(eng, B)
dzOnRadius = dz/find_radius(eng, B)
n_m = 10000000 #number of macro-particles

photon_energies = []


for i in range(n_m):
    result, photon_energy = photon_generator.synrad_0_no_spin_flip(upsilonSingleP, eng, dzOnRadius)
    if result == 1:
        photon_energies.append(photon_energy)

#%% Plotting histogram 
import matplotlib.pyplot as plt

photon_data = photon_energies
N_photons= len(photon_data)
# Set up the histogram parameters
bin_no = 500
dE = (np.max(photon_data) - np.min(photon_data)) / bin_no

# Create the figure and axes objects
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Plot the histogram of photon energies
# Plot 1/N dN/dE
H, bins = np.histogram(np.abs(photon_data), bins=bin_no)
ax[0].plot(bins[:-1], H / N_photons / dE, label='Photon Data from Python')
ax[0].set_xlabel('E [GeV]', fontsize=14)
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlim(0.1, 100)
ax[0].set_title('1/N dN/dE photons', fontsize=14)
ax[0].legend()
ax[0].grid()

# Plot 1/N d(E*N)/dE
H_weighted, bins_weighted = np.histogram(np.abs(photon_data), bins=bin_no, weights=np.abs(photon_data))
ax[1].plot(bins_weighted[:-1], H_weighted / N_photons / dE, label='Photon Data from Python')
ax[1].set_xlabel('E [GeV]', fontsize=14)
ax[1].set_xlim(0, 55)
ax[1].set_title('1/N d(E*N)/dE photons', fontsize=14)
ax[1].legend()
ax[1].grid()

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
