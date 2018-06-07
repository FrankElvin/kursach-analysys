#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:10:58 2017

@author: Nikita.Zhdanov
"""
from math import atan
from numpy import linspace, degrees, arctan
from pickle import load, dump
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

earth_data = 'const2/earth_const_data.pkl'
missile_data = 'const2/missile_const_data.pkl'
start_case = 'start_cond/standart_mesh/start_range2200_heigth2000.pkl'
bearing_case = 'flight_cond/bearing.pkl'

start_case_folder = 'start_cond/standart_mesh/'

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

if __name__ == '__main__':
	print "Initial height:\t%g m\nInitial range:\t%g m" %(Y_0, X_target)
	print "Max time of maneuver: %.2f sec" %(max_maneuver_time)
	print '-' * 70
	print "Maneuver time, sec | Angle of penetration, deg | Max wing overload, G"
	print '-' * 70

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

            print "%.2f\t\t\t%.2f\t\t\t%.2f " %(max_maneuver_time - 0.2*i, degrees(alpha), max(eta_k))

	    # if its a stop
            if max(eta_k) >= max_overload or degrees(alpha) <= 2.:
	    	print 'Too much overload. This is the optimum.'
	    	break
            else:
                out = alpha, max(eta_k)

            print "get overload"
	    i += 1

        except:
            print "Something gone wrong"
            break

print "X and Y lengthes: ", len(X), len(Y)
result_file = open('out_one_traektory.pkl', 'wb')
arr = [ X, Y]
dump(arr, result_file)
result_file.close()

if out:
    print "Initial point: {height:%g, range:%g};\nBest angle: %.2f deg with overload %2f" %(Y_0, X_target, degrees(out[0]), out[1])
else:
    print "Bad count. Initial point: {height:%g, range:%g};\nBest angle: %.2f deg with overload %2f" %(Y_0, X_target, degrees(alpha), max(eta_k))
print '-' * 70
