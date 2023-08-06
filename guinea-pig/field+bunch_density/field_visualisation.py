# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 23:53:28 2023

@author: william
"""
import numpy as np 
import matplotlib.pyplot as plt
field_data = np.loadtxt('C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/ILC-250GeV/10k_macroparticles/field.txt')
position_data = np.loadtxt('C:/Users/willi/OneDrive/Desktop/Beam-Beam-Interaction-Summer-Project/guinea-pig/ILC-250GeV/10k_macroparticles/beam_particle_position.txt')


#%% 
beam_data = position_data

number_entries = len(field_data) // 320

#Empty list of x y z 
x, y, z =[], [], []
E_x, E_y, E_z = [], [], []
B_x, B_y, B_z = [], [], []

# Divide the position into timesteps
for i in range(320):
    start = i * number_entries
    end = (i + 1) * number_entries

    # Slice beam_data for position information
    x_time_step = beam_data[start:end, 0]
    x.append(x_time_step)
    y_time_step = beam_data[start:end, 1]
    y.append(y_time_step)
    z_time_step = beam_data[start:end, 2]
    z.append(z_time_step)

    # Slice field_data for electric and magnetic fields information
    Ex_time_step = field_data[start:end, 0]
    E_x.append(Ex_time_step)
    Ey_time_step = field_data[start:end, 1]
    E_y.append(Ey_time_step)
    Ez_time_step = field_data[start:end, 2]
    E_z.append(Ez_time_step)

    Bx_time_step = field_data[start:end, 3]
    B_x.append(Bx_time_step)
    By_time_step = field_data[start:end, 4]
    B_y.append(By_time_step)
    Bz_time_step = field_data[start:end, 5]
    B_z.append(Bz_time_step)

#%% Plotting field
from scipy.interpolate import griddata
c = 3e+8 
# Using data from a specific timestep (e.g., timestep 0)
progress = 0.01
k = int(0.1*320) - 1
x_data, y_data, z_data = x[k], y[k], z[k]
Ex_data = E_x[k]*1e+18
Ey_data = E_y[k]*1e+18
Bx_data = B_x[k]*c
By_data = B_y[k]*c


# Create a figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
cmap = 'seismic'
# Plot E_x
sc1 = axs[0, 0].scatter(x_data, y_data, c=Ex_data, cmap=cmap)
axs[0, 0].set_title('E_x [V/m]')
axs[0, 0].set_ylabel('y [nm]')
fig.colorbar(sc1, ax=axs[0, 0])

# Plot E_y
sc2 = axs[0, 1].scatter(x_data, y_data, c=Ey_data, cmap=cmap)
axs[0, 1].set_title('E_y [V/m]')
fig.colorbar(sc2, ax=axs[0, 1])

# Plot B_x
sc3 = axs[1, 0].scatter(x_data, y_data, c=Bx_data, cmap=cmap)
axs[1, 0].set_title('B_x [T]')
axs[1, 0].set_ylabel('y [nm]')
axs[1, 0].set_xlabel('x [nm]')

fig.colorbar(sc3, ax=axs[1, 0])

# Plot B_y
sc4 = axs[1, 1].scatter(x_data, y_data, c=By_data, cmap=cmap)
axs[1, 1].set_title('B_y [T]')
axs[1, 1].set_xlabel('x [nm]')
fig.colorbar(sc4, ax=axs[1, 1])

# Display the plots
plt.tight_layout()
plt.show()

