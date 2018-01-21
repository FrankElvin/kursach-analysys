from pickle import dump
from math import radians

# basic bearing function
def line_bearing(t, initial_bearing, maneuver_start, maneuver_end):
	maneuver_interval = maneuver_end - maneuver_start
	if t < maneuver_start:
		return radians(initial_bearing)
	elif maneuver_start <= t < maneuver_end:
		return radians(
			maneuver_end*initial_bearing / maneuver_interval - 
			initial_bearing/maneuver_interval * t
		)
	else:
		return 0

# change bearing with parabolic law
def para_bearing(t, initial_bearing, maneuver_start, maneuver_end):
	t1 = maneuver_start 
	t2 = maneuver_end
	h1 = initial_bearing; h2 = 0
	a = (h1 - h2) / ( (t1**2-t2**2) - 2*(t1**2-t1*t2) )
	b = -2*a*t1; c = h1 - a*t1**2 - b*t1
	if t < t1:
		return radians(initial_bearing)
	elif t1 <= t < t2:
		return radians(a*t**2 + b*t + c)
	else:
		return 0