# -*- coding: utf-8 -*-
"""

Visualising bunch density with guinea-pig

Created on Wed Aug  2 18:57:50 2023

@author: william
"""



#%% INTERSECTION PLANE ONLY (x y extrapolated back)
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8, 3))  # Set width=8 inches and height=6 inches

path1 = 'C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/ILC-250GeV/100k_macroparticles/beam1.dat'
path2 = 'C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/ILC-250GeV/100k_macroparticles/beam2.dat'
# Load data from the files for both beams
beam_data_1 = np.loadtxt(path1)
beam_data_2 = np.loadtxt(path2)

# Access each column with appropriate names for both beams
x1 = beam_data_1[:, 1]  # x [um] for beam 1
y1 = beam_data_1[:, 2]  # y [um] for beam 1

x2 = beam_data_2[:, 1]  # x [um] for beam 2
y2 = beam_data_2[:, 2]  # y [um] for beam 2

# Combine the x and y coordinates from both beams
x_combined = np.concatenate((x1, x2))
y_combined = np.concatenate((y1, y2))

# Calculate the weights based on the scaling factor
scaling_factor = 2e+10 / 1e+5
weights_combined = np.ones_like(x_combined) * scaling_factor

# Create a 2D histogram with contour plot for combined data
plt.hist2d(x_combined, y_combined, bins=100, cmap='RdGy', weights=weights_combined)

# Add color bar for density representation
plt.colorbar(label='number of beam particles')

# Set axis labels and title
plt.xlabel('x [$\mu m$]')
plt.ylabel('y [$\mu m$]')
plt.title(r'$\rho_e+\rho_p$ beams')
plt.ylim(-0.06,0.06)
# Display the plot
plt.show()

#%% AT EACH TIMESTEP 
beam_data= np.loadtxt('C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/ILC-250GeV/100k_macroparticles/beam_particle_position.txt')
#%% Dividing into timesteps

#There are 1e+5 macro-particles with 320 timesteps 
 
number_entries = len(beam_data) // 320

# Create a list to store the upsilon into time steps
upsilon_step = []

#Empty list of x y z 
x =[]
y =[]
z =[]
# Divide the data into timesteps
for i in range(320):
    start = i * number_entries
    end = (i + 1) * number_entries
    x_time_step = beam_data[start:end, 0]
    x.append(x_time_step)
    y_time_step = beam_data[start:end, 1]
    y.append(y_time_step)
    z_time_step = beam_data[start:end, 2]
    z.append(z_time_step)


k = 200
# Calculate the weights based on the scaling factor
scaling_factor = 2e+10 / 1e+5
weights_combined = np.ones_like(x[k]) * scaling_factor

# Create a 2D histogram with contour plot for combined data
plt.hist2d(x[k], y[k], bins=100, cmap='RdGy', weights=weights_combined)

# Add color bar for density representation
plt.colorbar(label='number of beam particles')

# Set axis labels and title
plt.xlabel('x [$\mu m$]')
plt.ylabel('y [$\mu m$]')
plt.title(r'$\rho_e+\rho_p$ beams')
# Display the plot
plt.savefig('2D_density_plot.png',dpi=500)
plt.show()