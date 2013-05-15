article.pdf: article.tex assessingformula.tex assessingvisual.tex 3x3table.tex
	pdflatex article

3x3table.tex: ../data gen3x3Table.py
	python gen3x3Table.py > $@
