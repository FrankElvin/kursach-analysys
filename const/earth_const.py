# constatns of the Earth
from numpy import interp

def C43(a):
	cs = [0, 0.4, 0.6, 0.7, 0.8, 0.8, 0.9, 0.9, 1, 1.0, 1.1, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.4, 4.8, 5]
	k  = [0.152, 0.154, 0.155, 0.156, 0.164, 0.175, 0.196, 0.243, 0.327, 0.36, 0.374, 0.381, 0.384, 0.371, 0.355, 0.335, 0.32, 0.306, 0.292, 0.282, 0.273, 0.265, 0.262, 0.259, 0.257, 0.256, 0.255, 0.255, 0.254, 0.254 ]
	return interp(a, cs, k)

h =  [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
ro = [1.188, 1.165, 1.143, 1.121, 1.099, 1.078, 1.057, 1.037, 1.015, 0.996, 0.976, 0.928, 0.881, 0.837, 0.794, 0.753, 0.713]
cs = [340.2, 339.4, 338.6, 337.9, 337.1, 336.3, 335.5, 334.8, 333.9, 333.2, 332.4, 330.4, 328.5, 326.5, 324.5, 322.4, 320.4 ]
p  = [101323, 98943, 96609, 94319, 92074, 89872, 87713, 85596, 83521, 81487, 79493, 74680, 70106, 65761, 61637, 57725, 54016 ]

def ro_h(h_): return interp(h_, h, ro)
def cs_h(h_): return interp(h_,h,cs)
def p_h(h_): return interp(h_,h,p)

g = 9.81

# f = open('const_data.pkl', 'wb')
# arr = [ ro_h, cs_h, p_h, g ]
# f.close()

# print "File 'const_data.pkl' generated"
# raw_input('Press any key')