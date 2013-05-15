#!/usr/bin/python
import scipy.stats
x = []
y = []
for line in open('3x3.dat', "r"):
	n, fc, vc = map(float, line.split())
	x.append(vc)
	y.append(fc)

print "%.2f" % scipy.stats.pearsonr(x, y)[0] # ignore the p-value.
