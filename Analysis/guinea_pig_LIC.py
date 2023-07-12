# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:42:49 2023

@author: william

preliminary analysis on ILC parameters simulation from GP
"""

import read as rd

# Usage example


file = 'C:/Users/willi/OneDrive/Desktop/SULI Summer 2023/Analysis/ILC/ILC/ILC-350GeV/ILC-350GeV.out'  # Replace with your output file name

parser = rd.OutputParser(file)

results = parser.get_general_results()

lumi_ee_high_value = results['lumi_ee_high'] #daniel's unit 
f_rep=4.0
n_b=2450
f = f_rep*n_b #freq in Hz. Data from Snowmass paper 
print(lumi_ee_high_value)
print('GP luminosity 1% is',lumi_ee_high_value*f*1e-4, 'cm^{-2} s^{-1}' )


#%% Histogram attempt



import matplotlib.pyplot as plt
import math

def generate_center_of_mass_histogram(file_path):
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
                center_of_mass_energy = beam1_energy + beam2_energy
                center_of_mass_energies.append(center_of_mass_energy)

    # Determine the number of bins
    num_bins = int(math.sqrt(len(center_of_mass_energies)))

    # Create histogram
    plt.hist(center_of_mass_energies, bins=num_bins)

    # Customize the plot
    plt.xlabel('Center of Mass Energy (GeV)')
    plt.ylabel('Frequency')

    # Display the plot
    plt.show()
    plt.savefig("ILC-1TEV_A1_.png",dpi=500)



# Provide the file path as an argument to the function
file_path = 'C:/Users/willi/OneDrive/Desktop/SULI Summer 2023/Analysis/ILC/ILC/ILC-1TeV_A1_/lumi.gg.out'
generate_center_of_mass_histogram(file_path)


#%% 

def sum_final_column(file_path):
    total_frequency = 0
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                frequencies = line.split()
                # Assuming the frequency is the last value in each line
                frequency = float(frequencies[-1])
                total_frequency += frequency
    return total_frequency

# Provide the file path as an argument to the function
file_path = 'C:/Users/willi/OneDrive/Desktop/SULI Summer 2023/Analysis/ILC/ILC/ILC-1TeV_A1_/lumi.gg.out'
total_frequency = sum_final_column(file_path)
print("Total Frequency:", total_frequency*1e-10)
