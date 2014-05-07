#!/usr/bin/env python

def onebit(n):
  count = 0
  for _ in range(9):
    count += n & 1
    n >>= 1
  return count == 1

complexity = {}
for line in open('3x3.dat', "r"):
  n, _, vc = line.split()
  complexity[int(n)] = float(vc)

for i in range(512):
  for j in range(512):
    if onebit(i ^ j):
      print i, j, abs(complexity[i] - complexity[j])
