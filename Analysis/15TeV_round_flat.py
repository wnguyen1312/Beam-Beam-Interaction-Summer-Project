# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 22:46:05 2023

@author: william nguyen

An attempt to replicate results on the Snowmass paper. Round vs flat beam 15 TeV


"""


import read as rd

import numpy as np
import matplotlib.pyplot as plt
import math

file_flat = 'snowmass/PWFA_flat/PWFA_flat.out'  # Replace with your output file name
file_round = 'snowmass/PWFA_round/PWFA_round.out'
parser_flat = rd.OutputParser(file_flat)
parser_round = rd.OutputParser(file_round)

results_flat= parser_flat.get_general_results()
results_round = parser_round.get_general_results()

lumi_ee_high_value_flat = results_flat['lumi_ee_high'] #daniel's unit 
lumi_ee_high_value_round = results_round['lumi_ee_high'] #daniel's unit 

f_flat = 14000
f_round=2575 #freq in Hz. Data from Snowmass paper 
print('Flat beam: GP luminosity 1% is',lumi_ee_high_value_flat*f_flat*1e-4, 'cm^{-2} s^{-1}' )
print('Round beam: GP luminosity 1% is',lumi_ee_high_value_round*f_round*1e-4, 'cm^{-2} s^{-1}' )


#%% Histogram attempt



def generate_center_of_mass_histogram(file_paths):
    for file_path in file_paths:
        # Read data from file
        with open(file_path, 'r') as file:
            # Read each line and extract collision energies
            center_of_mass_energies = []
            for line in file:
                line = line.strip()
                if line:
                    energies = line.split()
                    beam1_energy = float(energies[0])
                    beam2_energy = float(energies[1])
                    center_of_mass_energy = 2*np.sqrt(beam1_energy* beam2_energy)
                    center_of_mass_energies.append(center_of_mass_energy)

        # Create histogram for current file
        plt.hist(center_of_mass_energies, bins='auto', histtype = 'step',linewidth=1.5,
                 label=file_path)

    # Customize the plot
    plt.xlabel('$E_{CM}$ [GeV]', fontsize = 18)
    plt.ylabel('Frequency', fontsize = 18)
    plt.yscale('log')
    plt.legend()
    plt.xlim(0,15000)
    plt.savefig('flat_round_15TeV_2.png',dpi=500)
    # Display the plot
    plt.show()

# Provide the file paths as a list of inputs to the function

file_path_flat = 'snowmass/PWFA_flat/lumi.ee.out'
file_path_round = 'snowmass/PWFA_round/lumi.ee.out'


file_paths = ['snowmass/PWFA_flat/lumi.ee.out', 'snowmass/PWFA_round/lumi.ee.out']

generate_center_of_mass_histogram(file_paths)



#normalise the y axis. convert to 1/cm^2 then Mutiply by frequency.  
#%% Luminosity spectra

def extract_center_of_mass_energies(file_paths):
    center_of_mass_energies_list = []
    
    for file_path in file_paths:
        # Read data from file
        with open(file_path, 'r') as file:
            # Read each line and extract collision energies
            center_of_mass_energies = []
            for line in file:
                line = line.strip()
                if line:
                    energies = line.split()
                    beam1_energy = float(energies[0])
                    beam2_energy = float(energies[1])
                    center_of_mass_energy = 2 * np.sqrt(beam1_energy * beam2_energy)
                    center_of_mass_energies.append(center_of_mass_energy)

        # Store center of mass energies for current file
        center_of_mass_energies_list.append(np.array(center_of_mass_energies))
    
    return center_of_mass_energies_list

# Provide the file paths as a list of inputs to the function
file_paths = ['snowmass/PWFA_flat/lumi.ee.out', 'snowmass/PWFA_round/lumi.ee.out']
center_of_mass_energies_list = extract_center_of_mass_energies(file_paths)

# Now you have a list of NumPy arrays, each containing the center of mass energies for each file
# You can analyze the data outside of this script as needed



E_flat = center_of_mass_energies_list[0]
E_round = center_of_mass_energies_list[1]
bin_no = 50
# Calculate the weights for E_flat
weights_flat = np.full_like(E_flat,  4.72109e+35 * 1e-4)
bin_width_flat = np.diff(np.histogram_bin_edges(E_flat, bins=bin_no))[0]

# Plot the histogram for E_flat with weighted y-values divided by bin width
plt.hist(E_flat, bins=bin_no, histtype='step', weights=weights_flat / bin_width_flat, label='flat beam')
plt.yscale('log')


# Plot the histogram for E_round
weights_round = np.full_like(E_round, 8.80492e+36 * 1e-4)
bin_width_round = np.diff(np.histogram_bin_edges(E_round, bins=bin_no))[0]

plt.hist(E_round, bins=bin_no, histtype='step', label='round beam', weights=weights_round / bin_width_round)
plt.yscale('log')

# Customize the plot
plt.xlabel('$E_{CM}$ [GeV]', fontsize=16)
plt.ylabel('Luminosity per bin [$cm^{-2} s^{-1} GeV^{-1}$]', fontsize=16)
plt.xlim(0,15000)
plt.legend()
plt.show()
plt.savefig('normalised_round_flat.png',dpi=500)
