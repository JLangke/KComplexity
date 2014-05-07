#!/usr/bin/env python

complexity = {}
for line in open('3x3.dat', "r"):
  n, _, vc = line.split()
  complexity[int(n)] = float(vc)

for i in range(512):
  for j in range(512):
    if i != j:
      print i, j, abs(complexity[i] - complexity[j])
