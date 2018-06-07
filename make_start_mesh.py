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
max_start_range = 3700
max_start_height = 4100
dx = 100

mesh_folder = 'start_cond/standart_mesh'

# clear mesh directory
for the_file in os.listdir(mesh_folder):
    file_path = os.path.join(mesh_folder, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)

print_progress(0, max_start_range-dx)
for start_range in range(2000, max_start_range, dx):
	for start_heigth in range(600, max_start_height, dx):
		Y_0 = start_heigth
		X_target = start_range

		outfile = open(mesh_folder + '/start_range%s_heigth%s.pkl' %(start_range, start_heigth), 'wb')
		dump( 
			( X_target, Y_target, V_target, V_0, mu_0, X_0, Y_0, t_oper ),
			outfile
		)
		outfile.close()
	print_progress(start_range, max_start_range-dx)
print "\nStandart launch mesh generated"
