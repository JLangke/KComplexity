#!/usr/bin/env python

complexity = {}
for line in open('3x3.dat', "r"):
  n, _, vc = line.split()
  complexity[int(n)] = float(vc)

for i in range(512):
  one = 0
  other = 0
  for x in range(2, -1, -1):
    for y in range(2, -1, -1):
      one <<= 1
      other <<= 1
      if i & (1 << (3*x + y)):
        one |= 1
      if i & (1 << (3*y + x)):
        other |= 1
  if one != other:
    print one, other, abs(complexity[one] - complexity[other])
