from pickle import load
from math import sin, cos, radians, atan
from numpy import array, linspace, concatenate, where, degrees, arctan, interp
from scipy import integrate

def get_traektory(earth_data, missile_data, start_case, bearing_case, bearing_fun):
	
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

	from const.earth_const import C43, ro_h, cs_h, p_h, g
	from const.bearing_styles import line_bearing, para_bearing
	from const.missile_const import i, I1, nu0, qm0, t_rdtt

	# Misc calculation
	A = g*nu0/I1

	# Time and initial condiditons
	t1 = linspace(t_rdtt[0], t_rdtt[1], 1000)[:-1]
	t2 = linspace(t_rdtt[1], t_oper[1], 1000)

	from earth_const import C43, ro_h, cs_h, p_h, g

	def dX1_dt(X, t=0):
		return array([
			g*nu0/(1-A*t) - i*C43(X[0]/cs_h(X[3]))*ro_h(X[3])*X[0]**2*g/(2*qm0*(1-A)) - g*sin(1.*atan((X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t)),
			A,
			X[0]*cos(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t)),
			X[0]*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t))
		])

	def dX2_dt(X, t=0):
		return array([
			- i*C43(X[0]/cs_h(X[3]))*ro_h(X[3])*X[0]**2*g/(2*qm0) - g*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t)),
			0,
			X[0]*cos(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t)),
			X[0]*sin(atan(1.*(X[3]-Y_target)/(X[2]-X_target))+bearing_fun(t))
		])

	# count init conditions
	NU_1 = [V_0, mu_0, X_0, Y_0]

	# first step of integration
	answer1 = integrate.odeint(dX1_dt, NU_1, t1)
	V1, mu1, X1, Y1 = answer1.T

	# recount init conditions
	NU_2 = [V1[-1], mu1[-1], X1[-1], Y1[-1]]

	# second step of integration
	answer2 = integrate.odeint(dX2_dt, NU_2, t2)
	answer2 = answer2[0: where(answer2[:,3]>0)[0][-1]]
	t2 = t2[0: where(answer2[:,3]>0)[0][-1]+1]
	V2, mu2, X2, Y2 = answer2.T

	# concatenate results
	V = concatenate( (V1[:-1], V2), axis=0)
	mu = concatenate( (mu1[:-1], mu2), axis=0)
	X = concatenate( (X1[:-1], X2), axis=0)
	Y = concatenate( (Y1[:-1], Y2), axis=0)
	t = concatenate((t1[:-1], t2), axis=0)

	return X, Y, V, mu, t