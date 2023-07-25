

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as scicon
import pxr_qed

print("pxr_qed is compiled in {:s} precision with {:s} units".
     format(pxr_qed.PRECISION, pxr_qed.UNITS))
if(pxr_qed.HAS_OPENMP):
    print("pxr_qed has openMP support!")
else:
    print("pxr_qed does not have openMP support!")
    
    
m_e = scicon.electron_mass
q_e = scicon.elementary_charge
hbar = scicon.hbar
c = scicon.c
um = scicon.micron
fs = scicon.femto
GeV = scicon.electron_volt*1.0e9

# Quantum Synchrotron radiation
def get_table(chi_min = 1.0e-3, chi_max = 10, frac_min = 1e-12, size=256):
    qs_photem_params = pxr_qed.qs.photon_emission_lookup_table_params()
    qs_photem_params.chi_part_min = chi_min
    qs_photem_params.chi_part_max = chi_max
    qs_photem_params.frac_min = frac_min
    qs_photem_params.chi_part_how_many = size
    qs_photem_params.frac_how_many = size
    qs_photon_emission_lookup_table = pxr_qed.qs.photon_emission_lookup_table(qs_photem_params)
    qs_photon_emission_lookup_table.generate()
    return qs_photon_emission_lookup_table


# This will take up to few minutes
qs_photon_emission_lookup_table_1em3_f10 = get_table(chi_min = 1.0e-3, chi_max = 10, frac_min = 1e-10, size=256)
qs_photon_emission_lookup_table_1em4_f10 = get_table(chi_min = 1.0e-4, chi_max = 10, frac_min = 1e-10, size=256)
qs_photon_emission_lookup_table_1em3_f12 = get_table(chi_min = 1.0e-3, chi_max = 10, frac_min = 1e-12, size=256)
qs_photon_emission_lookup_table_1em4_f12 = get_table(chi_min = 1.0e-4, chi_max = 10, frac_min = 1e-12, size=256)

qs_how_many = 1000000
qs_gamma = 1.9e5
Bz = 1e5

def get_energy_spectrum(qs_gamma, Bz, qs_how_many,table):
    qs_Ex = np.zeros(qs_how_many)
    qs_Ey = np.zeros(qs_how_many)
    qs_Ez = np.zeros(qs_how_many)
    qs_Bx = np.zeros(qs_how_many)
    qs_By = np.zeros(qs_how_many)
    qs_Bz = np.ones(qs_how_many)*Bz
    qs_px = np.ones(qs_how_many)*np.sqrt(qs_gamma**2-1)*m_e*c;
    qs_py = np.zeros(qs_how_many)
    qs_pz = np.zeros(qs_how_many)
    qs_rand = np.random.rand(qs_how_many)
    qs_ee = np.sqrt(1 + (qs_px**2 + qs_py**2 + qs_pz**2)/((m_e*c)**2))*m_e*c**2;
    qs_chi =  pxr_qed.chi_ele_pos(qs_px, qs_py, qs_pz, qs_Ex, qs_Ey, qs_Ez, qs_Bx, qs_By, qs_Bz)  
    
    qs_phot_px, qs_phot_py, qs_phot_pz = pxr_qed.qs.generate_photon_update_momentum(
        qs_chi, qs_px, qs_py, qs_pz, qs_rand, table)

    return np.sqrt(qs_phot_px**2 + qs_phot_py**2 + qs_phot_pz**2)*c

en_1em3_f10 = get_energy_spectrum(qs_gamma, Bz, qs_how_many,qs_photon_emission_lookup_table_1em3_f10)
en_1em4_f10 = get_energy_spectrum(qs_gamma, Bz, qs_how_many,qs_photon_emission_lookup_table_1em4_f10)
en_1em3_f12 = get_energy_spectrum(qs_gamma, Bz, qs_how_many,qs_photon_emission_lookup_table_1em3_f12)
en_1em4_f12 = get_energy_spectrum(qs_gamma, Bz, qs_how_many,qs_photon_emission_lookup_table_1em4_f12)

hist_1em3_f10, hen_1em3_f10 = np.histogram(en_1em3_f10/GeV, range=[1e-5,100], bins=1000)
hist_1em4_f10, hen_1em4_f10 = np.histogram(en_1em4_f10/GeV, range=[1e-5,100], bins=1000)
hist_1em3_f12, hen_1em3_f12 = np.histogram(en_1em3_f12/GeV, range=[1e-5,100], bins=1000)
hist_1em4_f12, hen_1em4_f12 = np.histogram(en_1em4_f12/GeV, range=[1e-5,100], bins=1000)

plt.loglog(0.5*(hen_1em3_f10[1:]+hen_1em3_f10[:-1]), hist_1em3_f10, label="chi_min = 1e-3, chi_frac_min=1e-10")
plt.loglog(0.5*(hen_1em4_f10[1:]+hen_1em4_f10[:-1]), hist_1em4_f10, label="chi_min = 1e-4, chi_frac_min=1e-10")
plt.loglog(0.5*(hen_1em3_f12[1:]+hen_1em3_f12[:-1]), hist_1em3_f12, label="chi_min = 1e-3, chi_frac_min=1e-12")
plt.loglog(0.5*(hen_1em4_f12[1:]+hen_1em4_f12[:-1]), hist_1em4_f12, label="chi_min = 1e-4, chi_frac_min=1e-12")
plt.xlabel("E (GeV)")
plt.ylabel("dN/dE")
plt.title("Photon spectrum")
plt.legend()
plt.savefig("res.png")
