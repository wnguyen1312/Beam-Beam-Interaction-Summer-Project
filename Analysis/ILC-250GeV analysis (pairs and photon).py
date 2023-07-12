# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 19:13:12 2023

@author: willi
"""

import read as rd
import numpy as np
import matplotlib.pyplot as plt

#lum value (L_0.1)
file_ILC_250GeV = 'ILC/final/ILC-250GeV.out'  # Replace with your output file name
parser_250GeV = rd.OutputParser(file_ILC_250GeV)
results_250GeV = parser_250GeV.get_general_results()

lumi_ee_high_value_250GeV = results_250GeV['lumi_ee_high'] #daniel's unit 

f = 6560 #f_rep mtuiplied by n_b 
print('250-GeV-ILC: GP luminosity 1% is',lumi_ee_high_value_250GeV*f*1e-4, 'cm^{-2} s^{-1}' )

#%% Luminosity spectra

# Provide the file paths as a list of inputs to the function
file_paths = ['ILC/final/lumi.ee.out' ]
center_of_mass_energies_list = rd.extract_center_of_mass_energies(file_paths)

E_250GeV = center_of_mass_energies_list[0]

bin_no = 200 #int(np.sqrt(len(E_250GeV)))
# Calculate the weights 
weights_250GeV = np.full_like(E_250GeV,  lumi_ee_high_value_250GeV * 1e-4)
bin_width_250GeV = np.diff(np.histogram_bin_edges(E_250GeV, bins=bin_no))[0]


# Plot the histogram for E_flat with weighted y-values divided by bin width
plt.hist(E_250GeV/250, bins=bin_no, histtype='step', weights=weights_250GeV / bin_width_250GeV, 
         label='250 GeV ILC')


plt.yscale('log')


# Customize the plot
plt.xlabel('$x = E_{CM}/max(E_{CM})$ ', fontsize=16)
plt.ylabel('Luminosity per bin [$cm^{-2} s^{-1} GeV^{-1}$]', fontsize=16)
plt.legend()
plt.show()

#%% Pairs spectra

file_paths_pairs = ['ILC/final/pairs.dat' ]
E_pairs = rd.extract_particle_energy(file_paths_pairs)[0]

weights_pairs= np.full_like(E_pairs,  1)
bin_width_pairs = np.diff(np.histogram_bin_edges(E_pairs, bins=bin_no))[0]

plt.hist(E_pairs, bins=bin_no, histtype='step', 
         weights=weights_pairs/bin_width_pairs, label='Incoherent pairs spectra 250 GeV')

# Customize the plot
plt.xlabel('$E_{e+e-}$ [GeV] ', fontsize=16)
plt.ylabel('$n_{e+e-}$ [$MeV^{-1}$]', fontsize=16)
plt.yscale('log')
plt.legend()
plt.show()
plt.savefig('C:\\Users\\willi\\OneDrive\\Desktop\\SULI Summer 2023\\Analysis\\figures\\pairs_250GeV_spectra')
#%% Photon spectra
bin_no = 200 #int(np.sqrt(len(E_250GeV)))

file_paths_photon = ['ILC/final/photon.dat' ]
E_photon = rd.extract_particle_energy(file_paths_photon)[0]

weights_photon= np.full_like(E_photon,  1)
bin_width_photon = np.diff(np.histogram_bin_edges(E_photon, bins=bin_no))[0]


plt.hist(E_photon, bins=bin_no, histtype='step', 
         weights=weights_photon/bin_width_photon, label='Photon energy spectra 250 GeV')

# Customize the plot
plt.xlabel('$E_{\gamma}$ [GeV]', fontsize=16)
plt.ylabel('$n_{\gamma}$ [$MeV^{-1}$]', fontsize=16) #number of photons per bin
plt.yscale('log')
plt.legend()
plt.show()
plt.savefig('C:\\Users\\willi\\OneDrive\\Desktop\\SULI Summer 2023\\Analysis\\figures\\photon_250GeV_spectra')