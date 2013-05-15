set terminal pdfcairo  size 5.00in, 3.00in 
set output '3x3scatter.pdf'
set border 3
set xlabel "TrueSkill rating of visual complexity (centered around 25)"
set ylabel "Formula complexity"
unset key
f(x) = m*x + b
fit f(x) '3x3.dat' using 3:2 via m,b
plot '3x3.dat' using ($3+rand(0)/2-.25):($2+rand(0)/2-.25), f(x)
