#!/usr/bin/env python
import gdbm
db = gdbm.open('kcomplexity.db', 'c')

import sys
for line in sys.stdin:
	kc, n, formula = line.split(" ", 2)
	db[n + "-kc"] = kc
	db[n + "-formula"] = formula
db.close()
