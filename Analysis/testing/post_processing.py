# -*- coding: utf-8 -*-
"""
File to test read.py file.

Created on Thu Jun 29 11:46:19 2023

Note: 
    - upsmax: max beamstrahlung parameter
    - luminosities are per bunch crossing and in m^-2 
@author: william nguyen
"""
import read as rd


# Usage example
output_filename = 'output_PWFA.out'  # Replace with your output file name
parser = rd.OutputParser(output_filename)

results = parser.get_general_results()

lumi_ee_high_value = results['lumi_ee_high'] #daniel's unit 
f = 4200 #freq in Hz. Data from Snowmass paper 

print('GP luminosity 1% is ',lumi_ee_high_value*f*1e-4, 'cm^{-2} s^{-1}')
