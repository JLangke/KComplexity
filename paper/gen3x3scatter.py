#!/usr/bin/python

fc = {}
vc = {}

for line in open("../data", "r"):
	c, n, _ = line.split(" ", 2)
	c = int(c)
	n = int(n)
	fc[n] = c

import gdbm
db = gdbm.open("../3x3survey/rankings.db", "r")
for i in range(512):
	key = str(i) + "-avg"
	if key in db:
		vc[i] = float(db[key])

for i in range(512):
	print i, fc.get(i, 17), vc.get(i, 25)
