#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:10:58 2017

@author: Nikita.Zhdanov
"""
from math import atan
from numpy import linspace, degrees, arctan
from pickle import load
from os import listdir

# Constant parameters
from const.earth_const import *

# Missile parameters
from const.missile_const import *

# all bearing styles
from const.bearing_styles import *

# function of max maneuver time
from modules.count_max_maneuver_time import get_max_maneuver_time

# function for traektory count
from modules.count_traektory import get_traektory

# function of overload count
from modules.count_overload import get_overload

# for demonstration of progress
from modules.progress_bar import print_progress

earth_data = 'const2/earth_const_data.pkl'
missile_data = 'const2/missile_const_data.pkl'
#start_case = 'start_cond/standart_mesh/start_range2000_heigth500.pkl'
bearing_case = 'flight_cond/bearing.pkl'

start_case_folder = 'start_cond/standart_mesh/'

result_file = open('result_file', 'w')
file_counter = 0
all_files = len(listdir(start_case_folder))

# show the beginning of the wariation
print ("Beginning the traektory variation.")
print_progress(0, all_files)

for start_case in listdir(start_case_folder):
    start_case = start_case_folder + start_case

    # Launch parameters
    launch_file = open(start_case, 'rb')
    launch_data = load(launch_file)
    X_target, Y_target, V_target, V_0, mu_0, X_0, Y_0, t_oper = launch_data
    launch_file.close()
    
    # Bearing parameters
    bearing_file = open(bearing_case, 'rb')
    bearing_data = load(bearing_file)
    t_bearing, max_bearing = bearing_data
    bearing_file.close()
    
    # Misc calculation
    A = g*nu0/I1
    
    # Time and initial condiditons
    t1 = linspace(t_rdtt[0], t_rdtt[1], 1000)[:-1]
    t2 = linspace(t_rdtt[1], t_oper[1], 1000)
    
    # Find initial time of maneuver
    max_maneuver_time = get_max_maneuver_time(start_case, bearing_case)[-1]

    # stop condition and step variable
    max_overload = 6.
    i = 0
    out = []

    # main variation
    while True:
    
        # Bearing by time
        def bearing(t):
            return para_bearing(t, max_bearing, t_rdtt[-1] + i*0.2, t_rdtt[-1] + max_maneuver_time)
    
        X, Y, V, mu, t = get_traektory(earth_data, missile_data, start_case, bearing_case, bearing)
    
        # for the bearing graph
        bear = map(bearing, t)
    
        try:
    	    # for overload count
    	    theta = arctan((Y-Y_target)/(X-X_target)) + [ bearing(x) for x in t ]
    	    eta, eta_k = get_overload(V, theta, t)

	    # for output
	    alpha = atan((X_target-X[-1])/Y[-1])

            # if its a stop
            if max(eta_k) >= max_overload or degrees(alpha) <= 2.:
                break
            else:
                out = alpha, max(eta_k)

            i += 1

        except:
            break
    
    if out:
        result_file.write('%g %g %.2f %2f 0\n' %(Y_0, X_target, degrees(out[0]), out[1]) )
    else:
        result_file.write('%g %g %.2f %2f 1\n' %(Y_0, X_target, degrees(alpha), max(eta_k)) )

    file_counter += 1

    print_progress(file_counter, all_files)
    #print '%d of %d files processed' %(file_counter, all_files)

result_file.close()
