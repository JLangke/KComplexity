#!/bin/bash

for i in `seq 0 511`
do
	python makepgm.py $i > $i.pgm
	convert -scale 30x30 $i.pgm $i.png
	rm $i.pgm
done
