#!/usr/bin/env python

def get(db, key, default):
	if key in db:
		return db[key]
	else:
		return default

def bit(b, n):
	return "#."[(n >> b) & 1]

def stringify(n):
	return bit(0, n) + bit(1, n) + "\n" + bit(2, n) + bit(3, n)

import cgi
import sys

import gdbm
db = gdbm.open("rankings.db", 'c')
data = []
for i in range(16):
	mu = float(get(db, str(i) + "-avg", 25))
	sig = float(get(db, str(i) + "-dev", 8.3333))
	data.append( (mu, i, sig) )

data.sort()
for mu, i, sigma in data:
	print "\n", stringify(i), i, mu, sigma
