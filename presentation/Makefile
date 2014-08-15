all: slides.pdf bridges.pdf

slides.pdf: slides.tex bib.bib *.png *.jpg */*.png
	pdflatex slides
	bibtex slides
	pdflatex slides
	pdflatex slides

bridges.pdf: bridges.tex *.png
	pdflatex bridges
	pdflatex bridges
	pdflatex bridges
