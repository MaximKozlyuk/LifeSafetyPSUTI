from math import sqrt

# not properly working draft

trz = 27.5
tnorm = 20.0
x = 0.35
vv = 1.5

t0 = tnorm - 1
print("t0 =", t0)

Pt = (trz-tnorm)/(trz-t0)
print("Pt =", Pt)

F0 = 0.32
m = 6.2
n = 5.1
e = 1.9

fs0 = ((x + 5.3 * Pt - 3.2)/(0.75 * n)) ** 2
b = fs0 < F0
print("f'0 =", fs0)
print("f'0 < F0:", b)

if not b:
  F0 = 0.64
  m = 6.2
  n = 5.1
  e = 1.9

  fs0 = ((x + 5.3 * Pt - 3.2)/(0.75 * n)) ** 2
  b = fs0 < F0
  print("f'0 =", fs0)
  print("f'0 < F0:", b)


if not b:
  F0 = 1.28
  m = 6.2
  n = 5.1
  e = 1.9

  fs0 = ((x + 5.3 * Pt - 3.2)/(0.75 * n)) ** 2
  b = fs0 < F0
  print("f'0 =", fs0)
  print("f'0 < F0:", b)

v0 = vv / (0.7 + 0.1 * (0.8 * m * sqrt(F0) - x))
print("v0 =", v0)

L0 = F0 * v0
print("L0 = ", L0)

XHt = 0.6 * n * sqrt(F0)
print("XHt = ", XHt)

tox = tnorm if x < XHt else trz - x * ((trz - tnorm) / XHt)
print("tox = ", tox)


Crz = 18.5
C0 = 9.0
PDK = 12.0







Pk = (Crz - PDK) / (Crz - C0)
print("Pk = ", Pk)

FS0 = ( (x + 3.7 * Pk - 1.5) / (0.75 * n) ) ** 2
print("FS0 = ", FS0)

V0 = vv / (0.55 + 0.14 * (0.8 * m * sqrt(F0) - x))
print("V0 = ", V0)

TOX = trz - (trz - tnorm) / (0.45 + 0.25 * (0.75 * n * sqrt(F0) - x))
print("TOX = ", TOX)