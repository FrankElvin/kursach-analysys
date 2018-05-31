#!/usr/bin/python2
from math import sin, cos, radians, atan, pi, degrees

def get_angle(x_missile, y_missile, x_target, y_target):
    angle = atan(
            abs(1.*y_missile - y_target)/
            abs(1.*x_missile - x_target))

    if x_missile <= x_target:
        return angle
    else:
        return pi - angle


# let us test
Vr = 10

# point 1
Xr = 5;  Yr = 10
Xc = 10; Yc = 0
dx = Vr * cos(get_angle(Xr, Yr, Xc, Yc))
dy = -Vr * sin(get_angle(Xr, Yr, Xc, Yc))
print ("\nMissile: {%s,%s};\nTarget: {%s,%s}" %(Xr,Yr, Xc,Yc))
print ("Counted angle as %.2f degrees"  %(degrees(get_angle(Xr, Yr, Xc, Yc))) )
print ("Then dx=%.2f dy = %.2f" %(dx, dy))


# point 2
Xr = 15;  Yr = 10
Xc = 10; Yc = 0
dx = Vr * cos(get_angle(Xr, Yr, Xc, Yc))
dy = -Vr * sin(get_angle(Xr, Yr, Xc, Yc))
print ("\nMissile: {%s,%s};\nTarget: {%s,%s}" %(Xr,Yr, Xc,Yc))
print ("Counted angle as %.2f degrees"  %(degrees(get_angle(Xr, Yr, Xc, Yc))) )
print ("Then dx=%.2f dy = %.2f" %(dx, dy))
