# -*- coding: utf-8 -*-
"""

Analysis of 250 GeV ILC 

Created on Thu Jul  6 18:28:40 2023

@author: william nguyen
"""

import read as rd

import numpy as np
import matplotlib.pyplot as plt

file_ILC_250GeV = 'ILC/ILC/ILC-250GeV/ILC-250GeV.out'  # Replace with your output file name

file_ILC_350GeV = 'ILC/ILC/ILC-350GeV/ILC-350GeV.out'

file_ILC_500GeV = 'ILC/ILC/ILCUPGRADE-500GeV/ILCUPGRADE-500GeV.out'

parser_250GeV = rd.OutputParser(file_ILC_250GeV)
parser_350GeV = rd.OutputParser(file_ILC_350GeV)
parser_500GeV = rd.OutputParser(file_ILC_500GeV)

results_250GeV = parser_250GeV.get_general_results()
results_350GeV = parser_350GeV.get_general_results()
results_500GeV = parser_500GeV.get_general_results()

lumi_ee_high_value_250GeV = results_250GeV['lumi_ee_high'] #daniel's unit 
lumi_ee_high_value_350GeV = results_350GeV['lumi_ee_high'] #daniel's unit 
lumi_ee_high_value_500GeV = results_500GeV['lumi_ee_high'] #daniel's unit 

f = 6560 #f_rep mtuiplied by n_b 
print('250-GeV-ILC: GP luminosity 1% is',lumi_ee_high_value_250GeV*f*1e-4, 'cm^{-2} s^{-1}' )


#%% Esimate of beamstrahlung compared to GP

#250 GeV
sigma_x_250GeV  = 515.48e-9
sigma_y_250GeV = 7.65916e-9 
sigma_z_250GeV = 300e-6 


f_rep = 5
n_b = 1312

beamstrahlung_250GeV = rd.find_beamstrahlung_average(2e+10, rd.find_gamma_electron(250/2), 
                                              sigma_x_250GeV, sigma_y_250GeV, sigma_z_250GeV)




beamstrahlung_max_250GeV = 12/5 * beamstrahlung_250GeV
n_photon_250_GeV = rd.estimate_photon( rd.find_gamma_electron(250/2), sigma_z_250GeV, beamstrahlung_250GeV )
n_photon_250_GeV_average = rd.estimate_photon_average(sigma_x_250GeV, 
                                                      sigma_y_250GeV, sigma_z_250GeV, 2e+10)
# print("Estimate of beamstrahlung parameter for 250 GeV is:", beamstrahlung_250GeV*f_rep*n_b)
print('Estimate of max beamstrahlung for 250 GeV is:', beamstrahlung_max_250GeV)
# print('Estimate of number of photons per particle for 250 GeV: ', n_photon_250_GeV_average)

#350 GeV
sigma_x_350GeV  = 683.52e-9
sigma_y_350GeV = 5.89474e-9 
sigma_z_350GeV = 300e-6 

f_rep_350GeV = 5 
n_b_350GeV = 1312

beamstrahlung_350GeV = rd.find_beamstrahlung_average(2e+10, rd.find_gamma_electron(350/2), 
                                              sigma_x_250GeV, sigma_y_250GeV, sigma_z_250GeV)



beamstrahlung_max_350GeV = 12/5 * beamstrahlung_350GeV


n_photon_350_GeV_average = rd.estimate_photon_average(sigma_x_350GeV, 
                                                      sigma_y_350GeV, 
                                                      sigma_z_350GeV, 2e+10)

# print("Estimate of beamstrahlung parameter for 350 GeV is:", beamstrahlung_350GeV*f_rep_350GeV*n_b_350GeV)
print('Estimate of max beamstrahlung for 350 GeV is:', beamstrahlung_max_350GeV)
# print('Estimate of number of photons per particle for 350 GeV: ', n_photon_350_GeV_average)


#500 GeV

sigma_x_500GeV  = 474.173e-9
sigma_y_500GeV = 5.85996e-9 
sigma_z_500GeV = 300e-6 

f_rep_500GeV = 5 
n_b_500GeV = 2625



beamstrahlung_500GeV = rd.find_beamstrahlung_average(2e+10, rd.find_gamma_electron(350/2), 
                                              sigma_x_500GeV, sigma_y_500GeV, sigma_z_500GeV)



beamstrahlung_max_500GeV = 12/5 * beamstrahlung_500GeV

n_photon_500_GeV_average = rd.estimate_photon_average(sigma_x_500GeV, 
                                                      sigma_y_500GeV, 
                                                      sigma_z_500GeV, 2e+10)

# print("Estimate of beamstrahlung parameter for 500 GeV is:", beamstrahlung_500GeV*f_rep_500GeV*n_b_500GeV)
print('Estimate of max beamstrahlung for 500 GeV is:', beamstrahlung_max_500GeV)


#%% Luminosity spectra

# Provide the file paths as a list of inputs to the function
file_paths = ['ILC/ILC/ILC-250GeV/lumi.ee.out','ILC/ILC/ILC-350GeV/lumi.ee.out', 'ILC/ILC/ILCUPGRADE-500GeV/lumi.ee.out'  ]
center_of_mass_energies_list = rd.extract_center_of_mass_energies(file_paths)

# Now you have a list of NumPy arrays, each containing the center of mass energies for each file
# You can analyze the data outside of this script as needed



E_250GeV = center_of_mass_energies_list[0]
E_350GeV = center_of_mass_energies_list[1]
E_500GeV = center_of_mass_energies_list[2]

bin_no = 200 #int(np.sqrt(len(E_250GeV)))
# Calculate the weights 
weights_250GeV = np.full_like(E_250GeV,  lumi_ee_high_value_250GeV * 1e-4)
bin_width_250GeV = np.diff(np.histogram_bin_edges(E_250GeV, bins=bin_no))[0]

weights_350GeV = np.full_like(E_350GeV,  lumi_ee_high_value_350GeV * 1e-4)
bin_width_350GeV = np.diff(np.histogram_bin_edges(E_350GeV, bins=bin_no))[0]

weights_500GeV = np.full_like(E_500GeV,  lumi_ee_high_value_500GeV * 1e-4)
bin_width_500GeV = np.diff(np.histogram_bin_edges(E_500GeV, bins=bin_no))[0]


# Plot the histogram for E_flat with weighted y-values divided by bin width
plt.hist(E_250GeV/250, bins=bin_no, histtype='step', weights=weights_250GeV / bin_width_250GeV, 
         label='250 GeV ILC')

plt.hist(E_350GeV/350, bins=bin_no, histtype='step', weights=weights_350GeV / bin_width_350GeV, 
         label='350 GeV ILC')


plt.hist(E_500GeV/500, bins=bin_no, histtype='step', weights=weights_500GeV / bin_width_500GeV, 
         label='500 GeV ILC Upgrade')
plt.yscale('log')


# Customize the plot
plt.xlabel('$x = E_{CM}/max(E_{CM})$ ', fontsize=16)
plt.ylabel('Luminosity per bin [$cm^{-2} s^{-1} GeV^{-1}$]', fontsize=16)
plt.legend()
plt.show()
plt.savefig('normILC_comparision.png',dpi=500)


