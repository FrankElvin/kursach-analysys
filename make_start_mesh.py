#!/usr/bin/python2.7
from pickle import dump
from modules.progress_bar import print_progress
import os

Y_target = 0
V_target = 0

V_0 = 31.6
mu_0 = 0.
X_0 = 0.

t_oper = [0, 40]
max_start_range = 4100

mesh_folder = 'start_cond/standart_mesh'

# clear mesh directory
for the_file in os.listdir(mesh_folder):
    file_path = os.path.join(mesh_folder, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)

print_progress(0, max_start_range)
for start_range in range(2100, max_start_range, 300):
	for start_heigth in range(600, 4100, 300):
		Y_0 = start_heigth
		X_target = start_range

		outfile = open(mesh_folder + '/start_range%s_heigth%s.pkl' %(start_range, start_heigth), 'wb')
		dump( 
			( X_target, Y_target, V_target, V_0, mu_0, X_0, Y_0, t_oper ),
			outfile
		)
		outfile.close()
	print_progress(start_range, max_start_range)
else:
	print_progress(start_range, max_start_range)

print "\nStandart launch mesh generated"
