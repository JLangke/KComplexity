#!/bin/bash

gnuplot <<EOF
set terminal pdfcairo  size 5.00in, 3.00in 
set output '$2'
set title "$1"
set ylabel "Fraction of comparisons"
set xlabel "Difference between the two artworks' strengths"
set border 1
plot './3x3allcomparisons.dat' using 2:1 with lines lw 2 title "PDF of distances between all artwork pairs", '$3' using 2:1 with linespoints lw 5 title "PDF of distances between $4"
EOF
