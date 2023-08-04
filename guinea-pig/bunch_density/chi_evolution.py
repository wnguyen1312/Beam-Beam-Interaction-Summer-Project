# -*- coding: utf-8 -*-
"""

Visualising chi evolution in GP

Created on Thu Aug  3 13:55:57 2023

@author: william

"""
import numpy as np
import matplotlib.pyplot as plt

upsilon_data = np.loadtxt('C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/photon_generation_test/upsilonSingleP.txt')

time_step_number = 16 * 20
n_m = 10e+3
expected_entries = 2 * n_m * time_step_number
dz = 3.28e-6
c = 3e+8
dt = dz / c

# Determine the number of entries per timestep
number_time_step = len(upsilon_data) // 320

# Create a list to store the upsilon into time steps
upsilon_step = []

# Divide the data into timesteps
for i in range(320):
    start = i * number_time_step
    end = (i + 1) * number_time_step
    upsilon_step_data = upsilon_data[start:end]
    upsilon_step.append(upsilon_step_data)

proportion_simulation = 0.55

k = int(proportion_simulation*len(upsilon_step)) -1
plt.hist(upsilon_step[k], bins=100)

# Calculate mean, max, min, and standard deviation for the kth time step
mean_value = np.mean(upsilon_step[k])
max_value = np.max(upsilon_step[k])
min_value = np.min(upsilon_step[k])
std_dev = np.std(upsilon_step[k])

# Add textbox with mean, max, min, and standard deviation information
plt.text(0.7, 0.9, f'Mean: {np.round(mean_value, 5)}\nMax: {np.round(max_value, 5)}\nMin: {np.round(min_value, 5)}\nStd Dev: {np.round(std_dev, 5)}',
         transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8))

plt.title(f'Time Step {k}, Real time {np.round(k*dt*1e+15,3)} fs')
plt.xlabel('$\chi$')
plt.ylabel('Frequency')

plt.show()


#%% Some summary plots

# Create a 2x5 subplot with 10 plots
fig, axs = plt.subplots(2, 5, figsize=(15, 8))
fig.suptitle('Histograms for Different Times in the Simulation', fontsize=16)

# Loop over different proportions and create subplots
for i, proportion_simulation in enumerate(np.linspace(0.1, 1.0, 10)):
    k = int(proportion_simulation * len(upsilon_step)) - 1
    ax = axs[i // 5, i % 5]  # Get the corresponding subplot axis
    ax.hist(upsilon_step[k], bins=50)
    mean_value = np.mean(upsilon_step[k])
    max_value = np.max(upsilon_step[k])
    min_value = np.min(upsilon_step[k])
    std_dev = np.std(upsilon_step[k])
    ax.set_title(f'Proportion: {proportion_simulation}\nMean: {np.round(mean_value, 5)}\nMax: {np.round(max_value, 5)}\nMin: {np.round(min_value, 5)}\nStd Dev: {np.round(std_dev, 5)}')
    ax.set_xlabel('$\chi$')
    ax.set_ylabel('Frequency')

plt.tight_layout()
plt.show()

#%% Evolution of max and average value (Guinea-Pig)

import numpy as np
import matplotlib.pyplot as plt

# Lists to store the mean and max chi values over real time
mean_chi_values = []
max_chi_values = []
min_chi_values = []
real_times = []

# Calculate mean and max chi values and real times for each time step
for i in range(len(upsilon_step)):
    mean_chi_values.append(np.mean(upsilon_step[i]))
    max_chi_values.append(np.max(upsilon_step[i]))
    min_chi_values.append(np.min(upsilon_step[i]))
    real_times.append(i * dt * 1e+12)  # Convert time step index to real time in femtoseconds

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Plot the evolution of max chi over real time
ax1.plot(real_times, max_chi_values, label='Max Chi')
ax1.set_ylabel('$\chi$')
ax1.set_title('Evolution of Max Chi over Real Time (Guinea-Pig)')
ax1.legend()
ax1.grid(True)

# Plot the evolution of min chi over real time
ax2.plot(real_times, min_chi_values, label='Min Chi')
ax2.set_xlabel('Real Time (ps)')
ax2.set_ylabel('$\chi$')
ax2.set_title('Evolution of Min Chi over Real Time (Guinea-Pig)')
ax2.legend()
ax2.grid(True)

# Adjust layout to prevent clipping of titles and labels
plt.tight_layout()

# Save the plot as 'chi_evolution_subplots.png' with high dpi
plt.savefig('chi_evolution_subplots_GP.png', dpi=500)

# Show the plot
plt.show()


#%% Evolution of max and average value (WarpX)
import pandas as pd
import matplotlib.pyplot as plt

CollDiagFname = 'C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/warpx/ColliderRelevant_beam_e_beam_p.txt'
df = pd.read_csv(CollDiagFname, sep='\s+', header=0)

# Assuming 'time(s)' is the time column in the DataFrame
time_column = df['[1]time(s)'].to_numpy()

# Accessing the 'chimax' columns for beam_e and beam_p
chimax_beam_e_columns = [col for col in df.columns if 'chimax_beam_e' in col]
chimax_beam_p_columns = [col for col in df.columns if 'chimax_beam_p' in col]

# Accessing the 'chimin' columns for beam_e and beam_p
chimin_beam_e_columns = [col for col in df.columns if 'chimin_beam_e' in col]
chimin_beam_p_columns = [col for col in df.columns if 'chimin_beam_p' in col]

# Extracting 'chimax' and 'chimin' values as NumPy arrays
chimax_beam_e = df[chimax_beam_e_columns].to_numpy()
chimax_beam_p = df[chimax_beam_p_columns].to_numpy()
chimin_beam_e = df[chimin_beam_e_columns].to_numpy()
chimin_beam_p = df[chimin_beam_p_columns].to_numpy()

# Creating the figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plotting chimax for beam_e and beam_p in the first subplot
for i, col_name in enumerate(chimax_beam_e_columns):
    ax1.plot(time_column * 1e+12, chimax_beam_e[:, i], label=col_name)

for i, col_name in enumerate(chimax_beam_p_columns):
    ax1.plot(time_column * 1e+12, chimax_beam_p[:, i], label=col_name)

ax1.set_xlabel('Time (ps)')
ax1.set_ylabel('$\chi_{max}$')
ax1.set_title('Evolution of $\chi_{max}$ for electron and positron beams (warpX)')
ax1.legend()
ax1.grid(True)

# Plotting chimin for beam_e and beam_p in the second subplot
for i, col_name in enumerate(chimin_beam_e_columns):
    ax2.plot(time_column * 1e+12, chimin_beam_e[:, i], label=col_name)

for i, col_name in enumerate(chimin_beam_p_columns):
    ax2.plot(time_column * 1e+12, chimin_beam_p[:, i], label=col_name)

ax2.set_xlabel('Time (ps)')
ax2.set_ylabel('$\chi_{min}$')
ax2.set_title('Evolution of $\chi_{min}$ for electron and positron beams (warpX)')
ax2.legend()
ax2.grid(True)

# Adjusting layout and spacing
plt.savefig('chi_evolution_warpx')
plt.tight_layout()
plt.show()


