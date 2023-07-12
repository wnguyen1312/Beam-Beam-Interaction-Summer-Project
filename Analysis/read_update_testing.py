# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 14:42:35 2023

@author: willi
"""
# class OutputParser:
#     def __init__(self, filename):
#         self.filename = filename
#         self.parsed_data = self.parse_output_file()

#     def parse_output_file(self):
#         with open(self.filename, 'r') as file:
#             content = file.read()

#         parsed_data = {}

#         # Parse beam parameters
#         beam_parameters = self.parse_beam_parameters(content)
#         parsed_data['beam_parameters'] = beam_parameters

#         # Parse switches
#         switches = self.parse_switches(content)
#         parsed_data['switches'] = switches

#         # Parse grid parameters
#         grid_parameters = self.parse_grid_parameters(content)
#         parsed_data['grid_parameters'] = grid_parameters

#         # Parse general results
#         general_results = self.parse_general_results(content)
#         parsed_data['general_results'] = general_results

#         return parsed_data

#     def parse_beam_parameters(self, content):
#         beam_parameters = []
#         beam_start = content.find('beam parameter 1')
#         beam_end = content.find('-------------  beam parameter 2 ------------')
#         beam_content = content[beam_start:beam_end].strip()

#         beam_lines = beam_content.split('\n')
#         beam_params = {}
#         for line in beam_lines:
#             if ':' in line:
#                 key_value = line.strip().split(':')
#                 if len(key_value) == 2:
#                     key, value = key_value
#                     beam_params[key.strip()] = value.strip()
#             elif 'beam parameter' in line:
#                 beam_parameters.append(beam_params)
#                 beam_params = {}

#         # Add the last beam parameter
#         beam_parameters.append(beam_params)

#         return beam_parameters

#     def parse_switches(self, content):
#         switches = {}
#         switches_start = content.find('SWITCHES :')
#         switches_end = content.find('grid parameters')
#         switches_content = content[switches_start:switches_end].strip()

#         switch_lines = switches_content.split('\n')
#         for line in switch_lines:
#             if '=' in line:
#                 key_value = line.strip().split('=')
#                 if len(key_value) == 2:
#                     key, value = key_value
#                     switches[key.strip()] = value.strip()

#         return switches

#     def parse_grid_parameters(self, content):
#         grid_parameters = {}
#         grid_start = content.find('grid parameters')
#         grid_end = content.find('general results')
#         grid_content = content[grid_start:grid_end].strip()

#         grid_lines = grid_content.split('\n')
#         for line in grid_lines:
#             if '=' in line:
#                 key_value = line.strip().split('=')
#                 if len(key_value) == 2:
#                     key, value = key_value
#                     grid_parameters[key.strip()] = value.strip()

#         return grid_parameters

#     def parse_general_results(self, content):
#         results_start = content.find('general results')
#         results_end = len(content)
#         results_content = content[results_start:results_end].strip()

#         result_lines = results_content.split('\n')
#         general_results = {}
#         for line in result_lines:
#             if '=' in line:
#                 key_value = line.strip().split('=')
#                 if len(key_value) == 2:
#                     key, value = key_value
#                     key = key.strip()
#                     if not key.startswith('lumi[') and not '[' in key:
#                         # Remove units or additional text from the value
#                         value = value.split()[0]
#                         # Remove semi-colons from the value
#                         value = value.rstrip(';')
#                         try:
#                             # Convert value to float
#                             value = float(value)
#                         except ValueError:
#                             # Handle non-numeric values
#                             pass
#                         general_results[key] = value

#         return general_results

#     def get_switches(self):
#         return self.parsed_data['switches']

#     def get_grid_parameters(self):
#         return self.parsed_data['grid_parameters']

#     def get_general_results(self):
#         return self.parsed_data['general_results']

class OutputParser:
    def __init__(self, filename):
        self.filename = filename
        self.parsed_data = self.parse_output_file()

    def parse_output_file(self):
        with open(self.filename, 'r') as file:
            content = file.read()

        parsed_data = {}

        # Parse beam parameters
        beam_parameters_1, beam_parameters_2 = self.parse_beam_parameters(content)
        parsed_data['beam_parameters_1'] = beam_parameters_1
        parsed_data['beam_parameters_2'] = beam_parameters_2

        # Parse switches
        switches = self.parse_switches(content)
        parsed_data['switches'] = switches

        # Parse grid parameters
        grid_parameters = self.parse_grid_parameters(content)
        parsed_data['grid_parameters'] = grid_parameters

        # Parse general results
        general_results = self.parse_general_results(content)
        parsed_data['general_results'] = general_results

        return parsed_data

    def parse_beam_parameters(self, content):
        beam_parameters_1 = []
        beam_parameters_2 = []
        beam_start_1 = content.find('beam parameter 1')
        beam_start_2 = content.find('beam parameter 2')

        # Parse beam parameters of beam 1
        beam_end_1 = beam_start_2
        beam_content_1 = content[beam_start_1:beam_end_1].strip()
        beam_parameters_1 = self.parse_beam_parameters_helper(beam_content_1)

        # Parse beam parameters of beam 2
        beam_end_2 = content.find('SWITCHES :')
        beam_content_2 = content[beam_start_2:beam_end_2].strip()
        beam_parameters_2 = self.parse_beam_parameters_helper(beam_content_2)

        return beam_parameters_1, beam_parameters_2

    def parse_beam_parameters_helper(self, beam_content):
        beam_lines = beam_content.split('\n')
        beam_params = {}
        beam_parameters = []
        for line in beam_lines:
            if ':' in line:
                key_value = line.strip().split(':')
                if len(key_value) == 2:
                    key, value = key_value
                    beam_params[key.strip()] = value.strip()
            elif 'beam parameter' in line:
                if beam_params:
                    beam_parameters.append(beam_params)
                    beam_params = {}

        # Add the last beam parameter
        if beam_params:
            beam_parameters.append(beam_params)

        return beam_parameters

    def parse_grid_parameters(self, content):
        grid_parameters = {}
        grid_start = content.find('grid parameters')
        grid_end = content.find('beam1')
        grid_content = content[grid_start:grid_end].strip()
    
        grid_lines = grid_content.split('\n')
        for line in grid_lines:
            if '=' in line:
                key_values = line.split('=')
                for key_value in key_values:
                    key_value = key_value.strip()
                    if key_value.startswith(('n_x', 'n_y', 'n_z', 'n_t', 'n_m.1', 'n_m.2', 'cut_x', 'cut_y', 'cut_z')):
                        key, _, value = key_value.partition(' = ')
                        if ';' in value:
                            value = value.rstrip(';')
                        grid_parameters[key] = value
    
        return grid_parameters
    



    # Remaining methods remain the same...
    def parse_switches(self, content):
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

        return switches



    def parse_general_results(self, content):
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

        return general_results

    def get_switches(self):
        return self.parsed_data['switches']

    def get_grid_parameters(self):
        return self.parsed_data['grid_parameters']

    def get_general_results(self):
        return self.parsed_data['general_results']

    def get_beam_parameters_1(self):
        return self.parsed_data['beam_parameters_1']

    def get_beam_parameters_2(self):
        return self.parsed_data['beam_parameters_2']


# Testing script
output_file = "ILC/ILC/ILC-350GeV/ILC-350GeV.out"

# Create an instance of OutputParser
parser = OutputParser(output_file)

# Test the methods
switches = parser.get_switches()
grid_parameters = parser.get_grid_parameters()
general_results = parser.get_general_results()
beam_parameters_1 = parser.get_beam_parameters_1()
beam_parameters_2 = parser.get_beam_parameters_2()

# Print the extracted data for verification
print("Switches:")
print(switches)
print("")

print("Grid Parameters:")
print(grid_parameters)
print("")

print("General Results:")
print(general_results)
print("")

print("Beam Parameters 1:")
print(beam_parameters_1)
print("")

print("Beam Parameters 2:")
print(beam_parameters_2)



