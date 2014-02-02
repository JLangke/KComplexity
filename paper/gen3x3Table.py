#!/usr/bin/python
import sys
from collections import defaultdict
seen = set()
data = defaultdict(list)
for line in open('../data', 'r'):
	size, n, _ = line.split(" ", 2)
	seen.add(int(n))
	data[int(size)].append(int(n))

print "\\begin{tabular}{r|l}"
print "FC & Artworks \\\\"
print "\\hline"
for i in range(1, max([k for k in data]) + 1):
	print i, "&",
	sys.stdout.write("\\reflectbox{\\rotatebox[origin=c]{180}{")
	for n in data[i]:
		sys.stdout.write("\\includegraphics[width=.06in]{3x3pics/%d.png}\\hspace{1pt}" % n)
	sys.stdout.write("}}")
	print "\\\\"

print "$\ge$", max([k for k in data]) + 1, "&",
for i in range(512):
	if i not in seen:
		sys.stdout.write("\\includegraphics[width=.06in]{3x3pics/%d.png}\\hspace{1pt}" % i)
print "\\end{tabular}"
