# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 14:14:59 2023

@author: william
"""

import read as rd
import numpy as np
import matplotlib.pyplot as plt

file = 'ultra_tight/NPQED.out'  # Replace with your output file name
parser = rd.OutputParser(file)



results = parser.get_general_results()

lumi_ee_high_value = results['lumi_ee_high'] #daniel's unit 

f = 100
print('GP luminosity 1% is',lumi_ee_high_value*f*1e-4, 'cm^{-2} s^{-1}' )
#%% Esimate of beamstrahlung compared to GP. Non-pertub QED so predictions are probably wrong

sigma_x = 10e-9
sigma_y = 10e-9 
sigma_z = 0.01e-6 



beamstrahlung = rd.find_beamstrahlung_average(8.75e+08, rd.find_gamma_electron(125/2), 
                                              sigma_x, sigma_y, sigma_z)

n_photon = rd.estimate_photon_average(sigma_x, sigma_y, sigma_z, 8.75e+08)


#%% Luminosity spectra

#%% Luminosity spectra

# Provide the file paths as a list of inputs to the function
file_paths = ['ultra_tight/lumi.ee.out' ]
center_of_mass_energies_list = rd.extract_center_of_mass_energies(file_paths)

# Now you have a list of NumPy arrays, each containing the center of mass energies for each file
# You can analyze the data outside of this script as needed



E = center_of_mass_energies_list[0]

bin_no = int(np.sqrt(len(E)))
# Calculate the weights 
weights = np.full_like(E,  lumi_ee_high_value * 1e-4)
bin_width = np.diff(np.histogram_bin_edges(E, bins=bin_no))[0]


# Plot the histogram for E_flat with weighted y-values divided by bin width
plt.hist(E/125, bins=bin_no, histtype='step', weights=weights/ bin_width, 
         label='Ultra tight bunches - 125 GeV')

plt.yscale('log')


# Customize the plot
plt.xlabel('$x = E_{CM}/max(E_{CM})$ ', fontsize=16)
plt.ylabel('Luminosity per bin [$cm^{-2} s^{-1} GeV^{-1}$]', fontsize=16)
plt.legend()
plt.show()
plt.savefig('ultra_tight_spectra.png',dpi=500)



