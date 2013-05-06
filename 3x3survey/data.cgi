#!/usr/bin/env python

import cgitb
cgitb.enable()

import random
import gdbm
rdb = gdbm.open("rankings.db", 'r')
kdb = gdbm.open("kcomplexity.db", 'r')

def get(db, i, key):
	key = str(i) + key
	if key in db:
		return float(db[key]) + random.random()*.5 - .25
	else:
		return 25 + random.random()*.5 - .25

print "Content-type: text/plain"
print
print "imageNumber\tvisualComplexity\tkolmogorovComplexity"
for i in range(512):
	print i, "\t", get(rdb, i, "-avg"), "\t", get(kdb, i, "-kc")
