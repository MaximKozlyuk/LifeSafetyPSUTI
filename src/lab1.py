import math

# not properly working draft

E = 1.9
d = 12.0
E1 = 1.5
E2 = 3.0
m1 = 0.381
m2 = 0.284
m = (((m2 - m1)*(E - E1))/(E2 - E1)) + m1
print("m = ", m)
md = m * d
print("md = ", md)

E1 = 1.0
E2 = 3.0

md1 = 2.0
md2 = 7.0

b11 = 2.85
b12 = 2.28
b21 = 10.0
b22 = 6.09

b1 = (((b12 - b11)*(E - E1))/(E2 - E1)) + b11
print("b1 = ", b1)

b2 = (((b22 - b21)*(E - E1))/(E2 - E1)) + b21
print("b2 = ", b2)

b = (((b2 - b1)*(md - md1))/(md2 - md1)) + b1
print("b = ", b)

a = 1/(b * math.exp(-md))
print("a = ", a)
