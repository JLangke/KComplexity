import sys

counts = {}
total = 0
for line in sys.stdin:
  count, n = map(int, line.split())
  counts[n] = count
  total += count

for n in counts:
  print counts[n] / float(total), n
