#!/usr/bin/python2.7
from pickle import dump

Y_target = 0
V_target = 0

V_0 = 31.6
mu_0 = 0.
X_0 = 0.

t_oper = [0, 40]

for start_range in range(2100, 4100, 100):
	for start_heigth in range(600, 4100, 100):
		Y_0 = start_heigth
		X_target = start_range

		outfile = open('start_cond/standart_mesh/start_range%s_heigth%s.pkl' %(start_range, start_heigth), 'wb')
		dump( 
			( X_target, Y_target, V_target, V_0, mu_0, X_0, Y_0, t_oper ),
			outfile
		)
		outfile.close()
	print "%.2f%% done." %( (22 - (4100 - start_range)/100.)*(100/21.) )

print "Standart launch mesh generated"
