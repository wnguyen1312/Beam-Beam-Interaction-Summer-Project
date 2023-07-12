# -*- coding: utf-8 -*-
"""
File to read the output of guinea-pig + some calculation functions


Created on Wed Jun 28 20:28:37 2023

@author: william nguyen
"""
import numpy as np 
# def parse_output_file(filename):
    
class OutputParser:
    def __init__(self, filename):
        self.filename = filename
        self.parsed_data = self.parse_output_file()

    def parse_output_file(self):
        with open(self.filename, 'r') as file:
            content = file.read()


        # Parse beam parameters
        beam_parameters = []
        beam_start = content.find('beam parameter 1')
        beam_end = content.find('-------------  beam parameter 2 ------------')
        beam_content = content[beam_start:beam_end].strip()
    
        beam_lines = beam_content.split('\n')
        beam_params = {}
        for line in beam_lines:
            if ':' in line:
                key_value = line.strip().split(':')
                if len(key_value) == 2:
                    key, value = key_value
                    beam_params[key.strip()] = value.strip()
            elif 'beam parameter' in line:
                beam_parameters.append(beam_params)
                beam_params = {}

        # Add the last beam parameter
        beam_parameters.append(beam_params)



        # Parse switches
        switches = {}
        switches_start = content.find('SWITCHES :')
        switches_end = content.find('grid parameters')
        switches_content = content[switches_start:switches_end].strip()

        switch_lines = switches_content.split('\n')
        for line in switch_lines:
            if '=' in line:
                key_value = line.strip().split('=')
                if len(key_value) == 2:
                    key, value = key_value
                    switches[key.strip()] = value.strip()

        # Parse grid parameters
        grid_parameters = {}
        grid_start = content.find('grid parameters')
        grid_end = content.find('general results')
        grid_content = content[grid_start:grid_end].strip()

        grid_lines = grid_content.split('\n')
        for line in grid_lines:
            if '=' in line:
                key_value = line.strip().split('=')
                if len(key_value) == 2:
                    key, value = key_value
                    grid_parameters[key.strip()] = value.strip()

        # Parse general results
        results_start = content.find('general results')
        results_end = len(content)
        results_content = content[results_start:results_end].strip()
    
        result_lines = results_content.split('\n')
        general_results = {}
        for line in result_lines:
            if '=' in line:
                key_value = line.strip().split('=')
                if len(key_value) == 2:
                    key, value = key_value
                    key = key.strip()
                    if not key.startswith('lumi[') and not '[' in key:
                        # Remove units or additional text from the value
                        value = value.split()[0]
                        # Remove semi-colons from the value
                        value = value.rstrip(';')
                        try:
                            # Convert value to float
                            value = float(value)
                        except ValueError:
                            # Handle non-numeric values
                            pass
                        general_results[key] = value


        return {
            'beam_parameters': beam_parameters,
            'switches': switches,
            'grid_parameters': grid_parameters,
            'general_results': general_results
        }


    def get_switches(self):
        return self.parsed_data['switches']

    def get_grid_parameters(self):
        return self.parsed_data['grid_parameters']

    def get_general_results(self):
        return self.parsed_data['general_results']

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

def find_gamma_electron(E): #energy in GeV


    m_e = 511 #mass of electron in keV
    
    
    gamma = E*1e+6 /m_e
    return gamma #this is where the error comes from 

def find_beamstrahlung_average(N, gamma, sigma_x, sigma_y, sigma_z):   
    r_e = 2.8179403262e-15 #classical electron radius
    alpha = 1/137
    beamstrahlung = 5/6 * N*r_e*r_e *gamma /(alpha*sigma_z*(sigma_x+sigma_y)
                              )
    return beamstrahlung

def estimate_photon(gamma, sigma_z, beamstrahlung):
    r_e = 2.8179403262e-15 #classical electron radius
    alpha = 1/137 
    return 2.54*alpha*alpha*sigma_z*beamstrahlung**(2/3) / (r_e*gamma)

def estimate_photon_average(sigma_x, sigma_y, sigma_z, N):
    r_e = 2.8179403262e-15 #classical electron radius
    alpha = 1/137 
    return 2.12 * alpha * r_e * N / (sigma_x + sigma_y)


def extract_particle_energy(filenames):
    energy_arrays = []
    for filename in filenames:
        energies = []
        with open(filename, 'r') as file:
            for line in file:
                values = line.strip().split()
                energy = float(values[0])
                energy = np.abs(energy)  # Ensure energy is positive
                energies.append(energy)
        
        energy_array = np.array(energies)
        energy_arrays.append(energy_array)
    
    return energy_arrays
