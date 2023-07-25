# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:45:03 2023
Replicating the photon generation (via beamstrahlung) guinea-pig but in Python
instead of C code. 

@author: william
"""

import math
import random

#constants

EMASS = (0.51099906/1000) #mass of electron in GeV

class RNDM:
    def __init__(self, seed=1):
        random.seed(seed)

    def rndm_synrad(self):
        return random.random()


def synradKi53andK23(x):
    "Function to approximate modified bessel functions"
    if x <= 1.54:
        x1 = x ** 0.6666666667
        x2 = x1 * x1
        x1inv = 1.0 / x1
        Ki53 = ((0.03363782042 * x1 - 0.1134842702) * x2 + 0.3944669710) * x2 - 1.812672515 + 2.1495282415344901 * x1inv
        K23 = (((0.04122878139 * x1 - 0.1494040962) * x2 + 0.7862616059) * x1 - 1.258219373) * x1 + 1.074647298 * x1inv
    elif x <= 4.48:
        Ki53 = ((0.09120815010 * x - 1.229105693) * x + 4.442223505) / (((x - 0.6903991322) * x + 5.651947051) * x - 0.9691386396)
        K23 = ((0.08194471311 * x - 1.112728296) * x + 4.052334415) / (((x - 0.6524469236) * x + 6.1800441958) * x - 0.4915880600)
    elif x <= 165.0:
        c = math.exp(-x) / math.sqrt(x)
        Ki53 = c * (2.187014852 + 1.253535946 * x) / (0.9949036186 + x)
        K23 = c * (0.6120387636 + 1.253322122 * x) / (0.3915531539 + x)
    else:
        Ki53 = 0.0
        K23 = 0.0

    return Ki53, K23

#ok let's assume field and calculate upsilon. M
#monoenergetic
#what is the photon spectrum given those conditions? 
#no time dependence 
#compute dz from energy and momentum. + check formula for radius 
#find dz/radius from that. 

def synrad_0_no_spin_flip(upsilonSingleP, eng, dzOnRadius):
    #x = 0.0
    #p0, p1, v1, v3, g = 0.0, 0.0, 0.0, 0.0, 0.0
    #fKi53, fK23 = 0.0, 0.0

    if eng <= 0.0:
        print("Initial particle energy below zero:", eng)
        return 1, 0.0  # Return both flag and photon energy as a tuple

    upsilon = float(upsilonSingleP)
    upsilon_bar = 1.5 * upsilon
    gamma = eng / EMASS  # Energy divided by mass of electron (in GeV)
    factor = (1.0 + 0.5 * upsilon_bar)**(1/3)
    p0 = 1.297210720417891e-02 * dzOnRadius * gamma / factor #dt: time interval = dz in GP 

    rndm_generator = random.random()  # This is p in the Japanese paper

    if rndm_generator > p0: #p vs p_0
        return 0, 0.0

    p1 = random.random()
    while True:
        v1 = random.random()
        if v1 != 0.0:
            break

    v3 = v1 * v1 * v1
    xden = 1.0 - v3 + 0.5 * upsilon_bar * (1.0 + v3 * v3)
    x = upsilon_bar * v3 / xden
    x1 = 1.0 - x
    z = x / (upsilon_bar * x1)
    fKi53, fK23 = synradKi53andK23(z)
    F00 = fKi53 + (x * x / x1) * fK23

    dxdy = 3.0 * v1 * v1 * (upsilon_bar + x * (1.0 - upsilon_bar * v3)) / xden
    g = F00 * dxdy * factor / (9.67287708690521 * upsilon)

    if p1 < g:
        photonEnergy = eng * x #formula 47
        return 1, photonEnergy
    else:
        photonEnergy = 0.0
        return 0, photonEnergy

