
from math import atan,degrees as deg_
from numpy import linspace, degrees, arctan, interp
from pickle import load

# function of max maneuver time
from count_max_maneuver_time import get_max_maneuver_time

# function for traektory count
from count_traektory import get_traektory

# function of overload count
from count_overload import get_overload

from const.earth_const import *
from const.bearing_styles import *
from const.missile_const import *

def get_best_angle(earth_data, missile_data, bearing_funs, start_case, bearing_case):

	# # Launch parameters
	launch_file = open(start_case, 'rb')
	X_target, Y_target, V_target, V_0, mu_0, X_0, Y_0, t_oper = load(launch_file)
	launch_file.close()

	# # Bearing parameters
	bearing_file = open(bearing_case, 'rb')
	t_bearing, max_bearing = load(bearing_file)
	bearing_file.close()

	# Misc calculation
	A = g*nu0/I1

	# Time and initial condiditons
	t1 = linspace(t_rdtt[0], t_rdtt[1], 1000)[:-1]
	t2 = linspace(t_rdtt[1], t_oper[1], 1000)

	# Find initial time of maneuver
	max_maneuver_time = get_max_maneuver_time(start_case, bearing_case)[-1]

	# if __name__ == '__main__':
	print "Initial height:\t%g m\nInitial range:\t%g m" %(Y_0, X_target)
	print "Max time of maneuver: %.2f sec" %(max_maneuver_time)
	print '-' * 70
	print "Maneuver time, sec | Angle of penetration, deg | Max wing overload, G"
	print '-' * 70

	# stop condition and step variable
	i = 0

	# main variation
	while True:

		# Bearing by time
		def bearing(t):
			return para_bearing(t, max_bearing, t_rdtt[-1] + i*0.2, t_rdtt[-1] + max_maneuver_time)

		X, Y, V, mu, t = get_traektory(earth_data, missile_data, start_case, bearing_case, bearing)

		# for the bearing graph
		bear = map(bearing, t)

		# for overload count
		theta = arctan((Y-Y_target)/(X-X_target)) + [ bearing(x) for x in t ]
		eta, eta_k = get_overload(V, theta, t)

		# for output
		alpha = atan((X_target-X[-1])/Y[-1])

		# if its a stop
		if max(eta_k) >= max_overload:
			break
		else:
			out = alpha, max(eta_k)

		i += 1

		if __name__ == '__main__':
			print "%.2f\t\t\t%.2f\t\t\t%.2f " %(max_maneuver_time - 0.2*i, degrees(alpha), max(eta_k))

	return Y_0, X_target, degrees(out[0]), out[1]
