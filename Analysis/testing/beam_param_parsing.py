# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:14:08 2023

@author: willi
"""
import re

# Function to extract beam parameters from a given section
def extract_beam_parameters(section):
    parameters = {}

    # Extract energy and number of particles
    energy_match = re.search(r"energy\s*:\s*([\d.]+)\s*GeV\s*;\s*particles\s*:\s*([\d.e+-]+)", section)
    if energy_match:
        parameters["energy"] = float(energy_match.group(1))
        parameters["particles"] = float(energy_match.group(2))

    # Extract sigma values
    sigma_match = re.search(r"sigma_x\s*:\s*([\d.]+)\s*nm\s*;\s*sigma_y\s*:\s*([\d.]+)\s*nm\s*;\s*sigma_z\s*:\s*([\d.]+)\s*micrometers", section)
    if sigma_match:
        parameters["sigma_x"] = float(sigma_match.group(1))
        parameters["sigma_y"] = float(sigma_match.group(2))
        parameters["sigma_z"] = float(sigma_match.group(3))

    # Extract emittance values
    emitt_match = re.search(r"emitt_x\s*:\s*([\d.]+)\s*emitt_y\s*:\s*([\d.]+)\s*\(([\w.]+)\)", section)
    if emitt_match:
        parameters["emitt_x"] = float(emitt_match.group(1))
        parameters["emitt_y"] = float(emitt_match.group(2))
        parameters["emitt_unit"] = emitt_match.group(3)

    # Extract beta values
    beta_match = re.search(r"beta_x\s*:\s*([\d.]+)\s*beta_y\s*:\s*([\d.]+)\s*\(([\w.]+)\)", section)
    if beta_match:
        parameters["beta_x"] = float(beta_match.group(1))
        parameters["beta_y"] = float(beta_match.group(2))
        parameters["beta_unit"] = beta_match.group(3)

    # Extract offset values
    offset_match = re.search(r"offset_x\s*:\s*([\d.-]+)\s*nm\s*;\s*offset_y\s*:\s*([\d.-]+)\s*nm\s*;\s*offset_z\s*:\s*([\d.-]+)\s*micrometers", section)
    if offset_match:
        parameters["offset_x"] = float(offset_match.group(1))
        parameters["offset_y"] = float(offset_match.group(2))
        parameters["offset_z"] = float(offset_match.group(3))

    # Extract waist values
    waist_match = re.search(r"waist_x\s*:\s*([\d.-]+)\s*waist_y\s*:\s*([\d.-]+)\s*\(([\w.]+)\)", section)
    if waist_match:
        parameters["waist_x"] = float(waist_match.group(1))
        parameters["waist_y"] = float(waist_match.group(2))
        parameters["waist_unit"] = waist_match.group(3)

    # Extract angle values
    angle_match = re.search(r"angle_x\s*:\s*([\d.-]+)\s*angle_y\s*:\s*([\d.-]+)\s*angle_phi\s*:\s*([\d.-]+)\s*\(([\w.]+)\)", section)
    if angle_match:
        parameters["angle_x"] = float(angle_match.group(1))
        parameters["angle_y"] = float(angle_match.group(2))
        parameters["angle_phi"] = float(angle_match.group(3))
        parameters["angle_unit"] = angle_match.group(4)

    # Extract distribution type and charge
    dist_match = re.search(r"type of distribution charge\s*:\s*([\w.]+)\s*dist_x\s*:\s*([\d.-]+)\s*dist_z\s*:\s*([\d.-]+)", section)
    if dist_match:
        parameters["distribution"] = dist_match.group(1)
        parameters["dist_x"] = float(dist_match.group(2))
        parameters["dist_z"] = float(dist_match.group(3))

    # Extract initial polarization (if present)
    polar_match = re.search(r"initial polarization\s*\(.+?\)\s*:\s*polar_x\s*=\s*([\d.-]+)\s*polar_y\s*=\s*([\d.-]+)\s*polar_z\s*=\s*([\d.-]+)", section)
    if polar_match:
        parameters["polar_x"] = float(polar_match.group(1))
        parameters["polar_y"] = float(polar_match.group(2))
        parameters["polar_z"] = float(polar_match.group(3))

    return parameters

# Read the output file
with open("output_PWFA.out", "r") as file:
    output_data = file.read()

# Find the sections describing Beam 1 and Beam 2
beam1_match = re.search(r"-+ beam parameter 1 -+\n\n([\s\S]+?)-+", output_data)
beam2_match = re.search(r"-+ beam parameter 2 -+\n\n([\s\S]+?)-+", output_data)

# Extract beam parameters for Beam 1
if beam1_match:
    beam1_section = beam1_match.group(1)
    beam1_params = extract_beam_parameters(beam1_section)
    print("Beam 1 Parameters:")
    print(beam1_params)

# Extract beam parameters for Beam 2
if beam2_match:
    beam2_section = beam2_match.group(1)
    beam2_params = extract_beam_parameters(beam2_section)
    print("Beam 2 Parameters:")
    print(beam2_params)

