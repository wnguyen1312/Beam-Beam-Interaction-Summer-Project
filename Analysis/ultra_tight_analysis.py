# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 12:32:57 2023


@author: william
"""

#%% estimate of beamstrahlung parameter
import numpy as np 
import read as rd
import matplotlib.pyplot as plt
#calculating gamma

E = 125/2 #in GeV
c = 3e+8 #speed of light
e = 1.6e-19 #charge of electron 
p = E*1e+6*e/c #SI unit. momentum
m_e = 9.11e-31 #mass of electron

A = p/(c*m_e) 
beta = A/np.sqrt(1+A*A) #relativistic beta 
gamma = 1/np.sqrt(1-beta*beta)
 

N = 0.0875e+10
r_e = 2.8179403262e-15 #classical electron radius
gamma = gamma #relativistic gamma
alpha = 1/137 
sigma_x = sigma_y = sigma_z = 10e-9  

beamstrahlung = 5/6 * N*r_e*r_e *gamma /(alpha*sigma_z*(sigma_x+sigma_y)
                                         )

beamstrahlung_max = 12/5 * beamstrahlung

print("Estimate of beamstrahlung parameter is:", beamstrahlung)
print('Estimate of max beamstrahlung is:', beamstrahlung_max)
#dimensionaless 



file = 'ultra_tight/NPQED.out'  # Replace with your output file name
parser = rd.OutputParser(file)

results= parser.get_general_results()

lumi_ee_high_value = results['lumi_ee_high'] #daniel's unit 

#%% Luminosity spectra

# Provide the file paths as a list of inputs to the function
file_paths = ['ultra_tight/lumi.ee.out']
center_of_mass_energies_list = rd.extract_center_of_mass_energies(file_paths)

# Now you have a list of NumPy arrays, each containing the center of mass energies for each file
# You can analyze the data outside of this script as needed



E_flat = center_of_mass_energies_list[0]
bin_no = int(np.sqrt(len(E_flat)))
# Calculate the weights for E_flat
weights_flat = np.full_like(E_flat,  lumi_ee_high_value * 1e-4)
bin_width_flat = np.diff(np.histogram_bin_edges(E_flat, bins=bin_no))[0]

# Plot the histogram for E_flat with weighted y-values divided by bin width
plt.hist(E_flat, bins=bin_no, histtype='step', weights=weights_flat / bin_width_flat, label='250 GeV ILC parameters')
plt.yscale('log')


# Customize the plot
plt.xlabel('$E_{CM}$ [GeV]', fontsize=16)
plt.ylabel('Luminosity per bin [$cm^{-2} s^{-1} GeV^{-1}$]', fontsize=16)
plt.legend()
plt.show()
plt.savefig('ultra_tight_bunch',dpi=500)