#!/usr/bin/env python

def get(db, key, default):
	if key in db:
		return db[key]
	else:
		return default

import cgitb
cgitb.enable()

import cgi
import sys

data = cgi.FieldStorage()
for k in ("winner", "loser"):
	if k not in data:
		sys.exit(0)
	try:
		int(data[k].value)
	except:
		sys.exit(0)

winner = data["winner"].value
loser = data["loser"].value

from trueskill import Rating, rate_1vs1
import gdbm
db = gdbm.open("rankings.db", 'c')

winMu = float(get(db, winner + "-avg", 25))
loseMu = float(get(db, loser + "-avg", 25))
winSigma = float(get(db, winner + "-dev", 8.3333))
loseSigma = float(get(db, loser + "-dev", 8.3333))

winRating, loseRating = rate_1vs1(Rating(winMu, winSigma), 
				  Rating(loseMu, loseSigma))

db[winner + "-avg"] = str(winRating.mu)
db[loser + "-avg"] = str(loseRating.mu)
db[winner + "-dev"] = str(winRating.sigma)
db[loser + "-dev"] = str(loseRating.sigma)

db.close()
del db

print "Content-type: text/plain"
print
print "{ winnerrating: %g, loserrating: %g }" % (winRating.mu, loseRating.mu)
