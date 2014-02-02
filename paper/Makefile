bridges_article.pdf: bibliography.bib bridges_article.tex 3x3table.tex 3x3scatter.pdf
	pdflatex bridges_article
	bibtex bridges_article
	pdflatex bridges_article
	pdflatex bridges_article

article.pdf: article.tex assessingformula.tex assessingvisual.tex 3x3table.tex 3x3scatter.pdf 3x3correlation.tex bibliography.bib
	pdflatex article
	bibtex article
	pdflatex article
	pdflatex article

3x3table.tex: ../data gen3x3Table.py
	python gen3x3Table.py > $@

3x3scatter.pdf: 3x3.dat 3x3.gnuplot
	gnuplot 3x3.gnuplot

3x3.dat: ../data ../3x3survey/rankings.db gen3x3scatter.py
	python gen3x3scatter.py > $@

3x3correlation.tex: correlationCoefficient.py 3x3.dat
	python correlationCoefficient.py > $@

clean:
	rm -f 3x3correlation.tex 3x3.dat 3x3scatter.pdf 3x3table.tex article.aux article.bbl article.blg article.log article.out article.pdf fit.log
