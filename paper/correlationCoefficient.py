#!/usr/bin/python
import sys
import scipy.stats
x = []
y = []
for line in open('3x3.dat', "r"):
	n, fc, vc = map(float, line.split())
	x.append(vc)
	y.append(fc)

print >>sys.stderr, scipy.stats.pearsonr(x, y)
print "%.2f" % scipy.stats.pearsonr(x, y)[0] # ignore the p-value.
