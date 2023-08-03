# -*- coding: utf-8 -*-
"""

Visualising bunch density with guinea-pig

Created on Wed Aug  2 18:57:50 2023

@author: william
"""


#%% Make a histogram in x, y, z 

import numpy as np
import matplotlib.pyplot as plt

# Load data from the file
beam_data = np.loadtxt('ILC/final/beam1.dat')

# Access each column with appropriate names
x = beam_data[:, 1]           # x [um]
y = beam_data[:, 2]           # y [um]
z = beam_data[:, 3]           # z [um]

N = len(beam_data)

# Create subplots for the histograms
fig, axes = plt.subplots(3, 1, figsize=(8, 12))
bin_no = 100

# Plot histogram for x
H, b = np.histogram(x, bins=bin_no)
axes[0].plot(0.5*(b[1:]+b[:-1]), H/N, color='blue', alpha=0.7)
axes[0].set_xlabel('x [um]')
axes[0].set_ylabel('Normalised frequency')

# Plot histogram for y
H, b = np.histogram(y, bins=bin_no)
axes[1].plot(0.5*(b[1:]+b[:-1]), H/N, color='green', alpha=0.7)
axes[1].set_xlabel('y [um]')
axes[1].set_ylabel('Normalised frequency')

# Plot histogram for z
H, b = np.histogram(z, bins=bin_no)
axes[2].plot(0.5*(b[1:]+b[:-1]), H/N, color='red', alpha=0.7)
axes[2].set_xlabel('z [um]')
axes[2].set_ylabel('Normalised frequency')

# Add a title for the whole plot
plt.suptitle('Beam particle distribution (beam 1) at the intersection plane')

# Adjust the layout to avoid overlapping titles and axis labels
plt.tight_layout()

# Display the plot
plt.savefig('distribution.png',dpi=500)
plt.show()

#%% 1D and 2D plots combined

# Create subplots for the histograms and 2D scatter plots
fig, axes = plt.subplots(3, 2, figsize=(12, 15))

# Scatter plot for (x, y)
axes[0, 0].scatter(x, y, s=5, c='blue', alpha=0.7)
axes[0, 0].set_xlabel('x [um]')
axes[0, 0].set_ylabel('y [um]')
axes[0, 0].set_title('(x, y) Scatter Plot')

# Scatter plot for (y, z)
axes[0, 1].scatter(y, z, s=5, c='green', alpha=0.7)
axes[0, 1].set_xlabel('y [um]')
axes[0, 1].set_ylabel('z [um]')
axes[0, 1].set_title('(y, z) Scatter Plot')

# Scatter plot for (x, z)
axes[1, 0].scatter(x, z, s=5, c='red', alpha=0.7)
axes[1, 0].set_xlabel('x [um]')
axes[1, 0].set_ylabel('z [um]')
axes[1, 0].set_title('(x, z) Scatter Plot')

# Histogram for x
bin_no = 100
H, b = np.histogram(x, bins=bin_no)
axes[1, 1].plot(0.5 * (b[1:] + b[:-1]), H / len(x), color='blue', alpha=0.7)
axes[1, 1].set_xlabel('x [um]')
axes[1, 1].set_ylabel('Normalized frequency')
axes[1, 1].set_title('Histogram for x')

# Histogram for y
H, b = np.histogram(y, bins=bin_no)
axes[2, 0].plot(0.5 * (b[1:] + b[:-1]), H / len(y), color='green', alpha=0.7)
axes[2, 0].set_xlabel('y [um]')
axes[2, 0].set_ylabel('Normalized frequency')
axes[2, 0].set_title('Histogram for y')

# Histogram for z
H, b = np.histogram(z, bins=bin_no)
axes[2, 1].plot(0.5 * (b[1:] + b[:-1]), H / len(z), color='red', alpha=0.7)
axes[2, 1].set_xlabel('z [um]')
axes[2, 1].set_ylabel('Normalized frequency')
axes[2, 1].set_title('Histogram for z')

# Adjust the layout to avoid overlapping titles and axis labels
plt.tight_layout()

# Display the plot
plt.savefig('scatter_and_histograms.png', dpi=500)
plt.show()

