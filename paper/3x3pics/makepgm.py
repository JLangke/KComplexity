#!/usr/bin/python

def bit(b, n):
	return (n >> b) & 1

import sys
n = int(sys.argv[1])

print "P2"
print 3, 3
print 16
for y in range(3):
	for x in range(3):
		print bit(y*3 + x, n)*10,
	print
