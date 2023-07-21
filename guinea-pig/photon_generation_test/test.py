# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:46:26 2023

@author: willi
"""

import random
import photon_generator
import matplotlib.pyplot as plt
import numpy as np

upsilonSingleP = 0.03  # Fixed upsilon value
eng = 125  # Fixed particle energy in GeV
Radius = 17  # Fixed radius

num_particles = 1000000  # Number of particles to test
dzOnRadius_values = np.logspace(-8, -6, num=50)  # Varying dzOnRadius between 1e-8 and 1e-6

probabilities = []

for dzOnRadius in dzOnRadius_values:
    photon_count = 0

    for _ in range(num_particles):
        result = photon_generator.synrad_0_no_spin_flip(upsilonSingleP, eng, dzOnRadius)
        
        if result == 1:
            photon_count += 1
    
    probability = photon_count / num_particles
    probabilities.append(probability)

# Plotting the results
plt.plot(dzOnRadius_values, probabilities, marker='o')
plt.xscale('log')
plt.xlabel('dzOnRadius')
plt.ylabel('Probability of Photon Generation')
plt.title('Effect of dzOnRadius on Probability of Photon Generation')
plt.grid(True)
plt.show()

#%%
import photon_generator
import numpy as np

# Read upsilonSingleP values from 'upsilon_table.txt'
upsilonSingleP_values = []

with open('upsilonSingleP.txt', 'r') as file:
    for line in file:
        upsilonSingleP_values.append(float(line.strip()))

# Read eng values from 'eng.txt'
eng_values = np.loadtxt('eng.txt')

# Read dzOnRadius values from 'dzOnRadius.txt'
dzOnRadius_values = np.loadtxt('dzOnRadius.txt')

# Get the length of the input tables
upsilon_table_length = len(upsilonSingleP_values)

photon_energies = []  # Store the generated photon energies

# Progress tracking settings
progress_interval = 1000  # Interval to print progress
total_iterations = upsilon_table_length
progress_count = 0

for i in range(upsilon_table_length):
    upsilonSingleP = upsilonSingleP_values[i]
    eng = eng_values[i]
    dzOnRadius = dzOnRadius_values[i]

    result, photon_energy = photon_generator.synrad_0_no_spin_flip(upsilonSingleP, eng, dzOnRadius)

    if result == 1:
        photon_energies.append(photon_energy)

    # Print progress
    progress_count += 1
    if progress_count % progress_interval == 0 or progress_count == total_iterations:
        progress_percent = (progress_count / total_iterations) * 100
        print(f"Progress: {progress_count}/{total_iterations} ({progress_percent:.2f}%)")

# Save the photon energies to 'photon_test.dat'
np.savetxt('photon_test.dat', photon_energies)

print("Photon energies saved to 'photon_test.dat'.")


#%% Plotting photon data
import numpy as np
import matplotlib.pyplot as plt

# Load data from 'photon_test.dat'
photon_data = np.loadtxt('photon_test.dat')

# Number of data points
N_photons = len(photon_data)
print(N_photons)
#%%
# Set up the histogram parameters
bin_no = 500
dE = (np.max(photon_data) - np.min(photon_data)) / bin_no

# Create the figure and axes objects
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Plot the histogram of photon energies
# Plot 1/N dN/dE
H, bins = np.histogram(np.abs(photon_data), bins=bin_no)
ax[0].plot(bins[:-1], H / N_photons / dE, label='Photon Data')
ax[0].set_xlabel('E [GeV]', fontsize=14)
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlim(0.1, 100)
ax[0].set_title('1/N dN/dE photons', fontsize=14)
ax[0].legend()
ax[0].grid()

# Plot 1/N d(E*N)/dE
H_weighted, bins_weighted = np.histogram(np.abs(photon_data), bins=bin_no, weights=np.abs(photon_data))
ax[1].plot(bins_weighted[:-1], H_weighted / N_photons / dE, label='Photon Data')
ax[1].set_xlabel('E [GeV]', fontsize=14)
ax[1].set_xlim(0, 55)
ax[1].set_title('1/N d(E*N)/dE photons', fontsize=14)
ax[1].legend()
ax[1].grid()

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
