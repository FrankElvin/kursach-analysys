from numpy import array, ediff1d, where
from math import cos,sin,asin,pi

def get_overload(V, theta, t):
	'''NOTE: return arrays are 1 element shorter than input'''

	dTheta = ediff1d(theta)
	dT = ediff1d(t)

	dV = []
	for i in range(len(V)-1):
		dV.append(V[i]**2 + V[i+1]**2 - 2*V[i]*V[i+1]*cos(dTheta[i]))

        # filter dV on zero values
        #for k in where(dV<10**-3):
        #    dV[k] = 0

	dV_k = []
	for i in range(len(V)-1):
		try:
			gamma = asin(V[i+1] * sin(dTheta[i]) / dV[i])
			if gamma <= pi /2.:
				dV_k.append(-dV[i]*sin(gamma))
			else:
				dV_k.append(-dV[i]*sin(pi-gamma))
		except:
			dV_k.append(0.)
	#	if dV[i] != 0:
	#		gamma = asin(V[i+1] * sin(dTheta[i]) / dV[i])
	#		if gamma <= pi /2.:
	#			dV_k.append(-dV[i]*sin(gamma))
	#		else:
	#			dV_k.append(-dV[i]*sin(pi-gamma))
	#	else:
	#		dV_k.append(0.)

	eta = array(dV) / dT / 9.81
	eta_k = array(dV_k) / dT / 9.81

	return eta, eta_k
