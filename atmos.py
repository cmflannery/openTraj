#!/usr/bin/env python
""" atmosCalc is used to compute atmospheric
    properties using 1976 standard atmosphere"""
import os
import subprocess
from pandas import read_table
import numpy as np
__author__ = "Cameron Flannery"
__copyright__ = "Copyright 2017"
__credits__ = ["Cameron Flannery"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Cameron Flannery"
__email__ = "cmflannery@ucsd.edu"
__status__ = "Development"


DEBUG = False

def calc_pressure(alt):
    # ============================================================================
    # LOCAL CONSTANTS
    # ============================================================================
    REARTH = 6369000.0      # radius of Earth (m)
    GMR = 0.034163195       # hydrostatic constant K/m
    NTAB = 8                # number of entries in the defining tables
    # ============================================================================
    # CREATE DATAFRAME (1976 STD. ATMOSPHERE)
    # ============================================================================
    path = os.path.join(os.getcwd(), 'atmosData.csv')
    df = read_table(path, delimiter=',', header=1,
                    dtype={'h(m)': np.float64, 'P(Pascal)': np.float64,
                           'T(K)': np.float64, 'dT(K/m)': np.float64})
    # * * * * * * * * * * * * * * Headers * * * * * * * * * * * * * *
    # i	h(m)	h(ft)	P(pascal)	P(inHg)	T(K)	dT(K/m)	dT(K/ft)
    h = alt*REARTH/(alt+REARTH)  # convert geometric to geopotential altitude
    htab = df['h(m)']       # create array with geopotential altitudes (m)
    gtab = df['dT(K/m)']    # Temperature Lapse Rate (K/m)
    ttab = df['T(K)']       # Standard Temperature (K)
    ptab = df['P(Pascal)']  # Static Pressure (Pascals)

    # Binary Search through htab data
    i = 0
    j = NTAB
    while True:
        k = (i+j)//2  # integer division
        if h < htab[k]:
            j = k
        else:
            i = k
        if j <= i+1:
            break

    tgrad = gtab[i]                                   # i will be in 1...NTAB-1
    tbase = ttab[i]
    deltah = h - htab[i]
    tlocal = tbase+tgrad*deltah  # local temperature
    theta = tlocal / ttab[0]  # ratio of temperature to sea-level temperature

    # delta =: ratio of pressure to sea-level pressure
    if tgrad == 0.0:
        delta = ptab[i] * np.exp(-GMR*deltah/tbase) / ptab[0]
    else:
        delta = ptab[i] * (tbase/tlocal)**(GMR/tgrad) / ptab[0]

    sigma = delta/theta  # ratio of density to sea-level density

    return (sigma, delta, theta)


def test_calc_pressure():
    print(calc_pressure(629.70))
    print(calc_pressure(30000))


if __name__ == '__main__':
    try:
        subprocess.call('clear')
    except OSError:
        subprocess.call('cls', shell=True)
    if DEBUG:
        test_calc_pressure()
