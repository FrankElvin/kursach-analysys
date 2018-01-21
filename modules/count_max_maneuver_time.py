# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:10:58 2017

@author: Nikita.Zhdanov
"""
from math import sin, cos, radians, atan, degrees
from scipy import integrate
from numpy import array, linspace, concatenate, where
from pickle import load
import const

# Constant parameters
from const.earth_const import *

# Missile parameters
from const.missile_const import *

# all bearing styles
from const.bearing_styles import *

start_case = 'start_cond/start.pkl'
bearing_case = 'flight_cond/bearing.pkl'

def get_max_maneuver_time(start_case, bearing_case):

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

	def dX1_dt(X, t=0):
		return array([
			g*nu0/(1-A*t) - i*C43(X[0]/cs_h(X[3]))*ro_h(X[3])*X[0]**2*g/(2*qm0*(1-A)) - g*sin(1.*atan((X[3]-Y_target)/(X[2]-X_target))+radians(max_bearing)),
			A,
			X[0]*cos(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+radians(max_bearing)),
			X[0]*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+radians(max_bearing))
		])

	def dX2_dt(X, t=0):
		return array([
			- i*C43(X[0]/cs_h(X[3]))*ro_h(X[3])*X[0]**2*g/(2*qm0) - g*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target))),
			0,
			X[0]*cos(atan(1.*(X[3]-Y_target)/(X[2]-X_target))),
			X[0]*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target)))
		])

	# count init conditions
	NU_1 = [V_0, mu_0, X_0, Y_0]

	# first step of integration
	answer1, infodict = integrate.odeint(dX1_dt, NU_1, t1, full_output=True)
	if __name__ == '__main__':
		print infodict['message']
	V1, mu1, X1, Y1 = answer1.T

	# recount init conditions
	NU_2 = [V1[-1], mu1[-1], X1[-1], Y1[-1]]

	# second step of integration
	answer2, infodict = integrate.odeint(dX2_dt, NU_2, t2, full_output=True)
	if __name__ == '__main__':
		print infodict['message']
	answer2 = answer2[0: where(answer2[:,3]>0)[0][-1]]
	t2 = t2[0: where(answer2[:,3]>0)[0][-1]+1]
	V2, mu2, X2, Y2 = answer2.T

	# results
	if __name__ == '__main__':
		print "Flight time: %.2f sec" %t2[-1]
		alpha = atan( (X_target-X2[-1])/Y2[-1] ) 
		print "Angle of penetration: %.2f degrees" %degrees(alpha)

		from matplotlib import pyplot as plt
		plt.plot(X1, Y1, label='Part 1')
		plt.plot(X2, Y2, label='Part 2')
		plt.legend(loc='best')
		plt.legend(loc='best')
		plt.xlabel('x, m')
		plt.ylabel('y, m')
		plt.xlim([0,4000]); plt.ylim([0,4000])
		plt.show()

	return X_target, Y_0, t2[-1] - t_rdtt[-1]

if __name__ == '__main__':
	pass
	# print "Max time of maneuver: %.2f sec" %(get_max_maneuver_time(start_case, bearing_case))