#!/usr/bin/env python

bits = 0x1F  # only the last 9 bits are important
complexity = {}
for line in open('3x3.dat', "r"):
  n, _, vc = line.split()
  complexity[int(n)] = float(vc)

for i in range(512):
  one = i
  other = (~i) & bits
  print one, other, abs(complexity[one] - complexity[other])
