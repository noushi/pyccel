# coding: utf-8

from numpy import zeros
from numpy import ones

a1 = zeros(64, double)
a2 = zeros(3,2)
a3 = zeros(5, int)
a4 = zeros((2,3), double)

b1 = ones(64, double)
b2 = ones(3,2)
b3 = ones(5, int)
b4 = ones((2,3), double)

c1 = array((1,2,3,5,8,5),int)
c2 = array(((5,8,6,9,8,2),(5,8,6,9,8,2),(5,8,6,9,8,2),(5,8,6,9,8,2),(5,8,6,9,8,2),(5,8,6,9,8,2)),int)

d0  = abs(-2.0)
d1  = sqrt(2.0)
d2  = sin (2.0)
d3  = cos (2.0)
d4  = tan (2.0)
#d5  = cot (2.0)
d6  = exp (2.0)
d7  = log (2.0)
d8  = asin(2.0)
#d9  = acsc(2.0)
d10 = acos(2.0)
#d11 = asec(2.0)
d12 = atan(2.0)
#d13 = acot(2.0)
d14 = atan(2.0)
#d15 = csc (2.0)
#d16 = sec (2.0)
d17 = ceil (2.2)

e   = 1.0
e0  = 3.0 + 2.0 * abs(e)
e1  = 3.0 + 2.0 * sqrt(e)
e2  = 3.0 + 2.0 * sin (e)
e3  = 3.0 + 2.0 * cos (e)
e4  = 3.0 + 2.0 * tan (e)
#e5  = 3.0 + 2.0 * cot (e)
e6  = 3.0 + 2.0 * exp (e)
e7  = 3.0 + 2.0 * log (e)
e8  = 3.0 + 2.0 * asin(e)
#e9  = 3.0 + 2.0 * acsc(e)
#e10 = 3.0 + 2.0 * acos(e)
#e11 = 3.0 + 2.0 * asec(e)
e12 = 3.0 + 2.0 * atan(e)
#e13 = 3.0 + 2.0 * acot(e)
e14 = 3.0 + 2.0 * atan(e)
#e15 = 3.0 + 2.0 * csc (e)
#e16 = 3.0 + 2.0 * sec (e)
e17 = 3.0 + 2.0 * ceil(e) # problem with check_compatibility with ints

#z1 = dot(c1, c1)
#z2 = 3.0 + 2.0 * dot(c1, c1)