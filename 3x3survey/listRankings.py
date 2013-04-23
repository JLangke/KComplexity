#!/usr/bin/env python

def get(db, key, default):
	if key in db:
		return db[key]
	else:
		return default

def bit(b, n):
	return "#."[(n >> b) & 1]

def stringify(n):
	return "\n".join([ "".join([bit(x+3*y, n) for x in range(3)]) for y in range(3) ])

import cgi
import sys

import gdbm
db = gdbm.open("rankings.db", 'c')
data = []
for i in range(512):
	mu = float(get(db, str(i) + "-avg", 25))
	sig = float(get(db, str(i) + "-dev", 8.3333))
	data.append( (mu, i, sig) )

data.sort()
for mu, i, sigma in data:
	print stringify(i), i, mu, sigma
