# -*- coding: utf-8 -*-
"""

Visualising bunch density with guinea-pig

Created on Wed Aug  2 18:57:50 2023

@author: william
"""



#%% INTERSECTION PLANE ONLY (x y extrapolated back)
import matplotlib.pyplot as plt
import numpy as np


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

progress = 1
k = int(progress*320)-1

# Calculate the weights based on the scaling factor
scaling_factor = 2e+10 / 1e+5
weights_combined = np.ones_like(x[k]) * scaling_factor

# Create a 2D histogram with contour plot for combined data
plt.hist2d(x[k], y[k], bins=100, cmap='RdGy_r', weights=weights_combined)

# Add color bar for density representation
plt.colorbar(label=r'$\rho_e+\rho_p$')

# Set axis labels and title
plt.xlabel('x [$\mu m$]')
plt.ylabel('y [$\mu m$]')
plt.title(r'$\rho_e+\rho_p$ beams')
# Display the plot
plt.savefig('2D_density_plot.png',dpi=500)
plt.show()
#%% Plotting in z,x and z,y
 
number_entries = len(beam_data) // 320

#Empty list of x y z 
x =[]
y =[]
z =[]

my_dpi=500
fig, ax = plt.subplots(1, 3,figsize=(6000./my_dpi, 2000./my_dpi))
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

progress = 0.8
k = int(progress*320)-1

# Calculate the weights based on the scaling factor
scaling_factor = 2e+10 / 1e+5
weights_combined = np.ones_like(x[k]) * scaling_factor

# Create a 2D histogram with contour plot for combined data
h1 = ax[0].hist2d(x[k], y[k], bins=100, cmap='RdGy_r', weights=weights_combined)
ax[1].hist2d(z[k]*1e-6, x[k], bins=100, cmap='RdGy_r', weights=weights_combined)
ax[2].hist2d(z[k]*1e-6, y[k], bins=100, cmap='RdGy_r', weights=weights_combined)

ax[0].set_xlabel('x [nm]')
ax[0].set_ylabel('y [nm]')
ax[0].set_title('xy density plot')

ax[1].set_xlabel('z [mm]')
ax[1].set_ylabel('y [nm]')
ax[1].set_title('zy density plot')

ax[2].set_xlabel('z [mm]')
ax[2].set_title('zx density plot')
ax[2].set_ylabel('x [nm]')

# Add color bar for density representation
cbar = plt.colorbar(h1[3], ax=ax, label=r'$\rho_e+\rho_p$')


# Display the plot
plt.show()


#%% Subplots

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# Make tick marks larger
plt.rcParams['xtick.major.size'] = 3
plt.rcParams['ytick.major.size'] = 3


# Assuming beam_data is available in the environment
number_entries = len(beam_data) // 320
my_dpi = 500

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

# Scaling factor
scaling_factor = 2e+10 / 1e+5

# Subplot progress indices
progress_steps = np.linspace(0, 1, 10)  # This will create 10 steps from 0 to 1

# Create a subplot grid
fig = plt.figure(figsize=(6000./my_dpi, 2000./my_dpi))
gs = gridspec.GridSpec(2, 6, width_ratios=[1, 1, 1, 1, 1, 0.05])  # 2 rows, 6 columns, last one for colorbar
gs.update(wspace=0.6)

# Create a 2D histogram with contour plot for combined data at each progress step
ax = {}
for idx, progress in enumerate(progress_steps):
    k = int(progress * 320) - 1
    weights_combined = np.ones_like(x[k]) * scaling_factor

    # Convert linear index to 2D index
    row = idx // 5  # Integer division will give us the row index
    col = idx % 5   # Modulo operation will give us the column index

    # Plot the histogram on the corresponding subplot axis
    if idx == 0:
        ax[idx] = plt.subplot(gs[row, col])
    else:
        ax[idx] = plt.subplot(gs[row, col], sharex=ax[0], sharey=ax[0])  # share x and y axes with the first subplot

    # If not on the bottom row, hide the x-axis labels
    if row != 1:  # If not on the bottom row
        plt.setp(ax[idx].get_xticklabels(), visible=False)

    im = ax[idx].hist2d(x[k], y[k], bins=100, cmap='RdGy_r', weights=weights_combined)

    # Set axis labels and title

    ax[idx].set_xlim(-1500, 1500)
    ax[idx].set_title(f'Time: t={progress:.1f}T')

ax[0].set_ylabel('y [nm]')
ax[5].set_ylabel('y [nm]')

for i in range(5,10):
    ax[i].set_xlabel('x [nm]')
    
# Add a colorbar to the right of the subplots
cbax = plt.subplot(gs[:,-1])  # Place it where it should be.
cb = plt.colorbar(im[3], cax=cbax)
cb.set_label(r'$\rho_e+\rho_p$')


# Display the plot
#plt.tight_layout()
plt.savefig('2D_density_plot.png',dpi=500)
plt.show()

#%% Make a video for fun

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Assuming beam_data is available in the environment
number_entries = len(beam_data) // 320

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

# Scaling factor
scaling_factor = 2e+10 / 1e+5

# Figure setup
fig, ax = plt.subplots()
ax.set_xlim(-1500, 1500)
ax.set_ylim(-30, 30)
ax.set_xlabel('x [nm]')
ax.set_ylabel('y [nm]')

# Animation update function
def update(frame):
    ax.cla()  # Clear the current axis
    ax.set_xlim(-1500, 1500)
    ax.set_ylim(-30, 30)
    ax.set_xlabel('x [nm]')
    ax.set_ylabel('y [nm]')
    k = frame * 20 
    weights_combined = np.ones_like(x[k]) * scaling_factor
    im = ax.hist2d(x[k], y[k], bins=100, cmap='RdGy_r', weights=weights_combined)
    ax.set_title(f'Time: t={k/320:.1f}T')

# Create animation
ani = animation.FuncAnimation(fig, update, frames=range(1, 16), interval=200)

# Save as gif
ani.save("animation.gif", writer='pillow', fps=30)

# Uncomment the line below if you want to save the animation as .mp4 movie and have ffmpeg installed
ani.save("animation.mp4", writer='ffmpeg', fps=30)
