# Create file that contains constatns of missile
from pickle import dump

i = 1.4
I1 = 2600.
nu0 = 6.
qm0 = 13000.

t_rdtt = [0, 4.5]

f = open('missile_const_data.pkl', 'wb')
arr = [ i, I1, nu0, qm0, t_rdtt ]
dump(arr, f)
f.close()

print "File 'missile_const_data.pkl' generated"
raw_input('Press any key')