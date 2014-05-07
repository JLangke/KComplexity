bridges_article.pdf: bibliography.bib bridges_article.tex 3x3table.tex 3x3scatter.pdf 3x3inversions.pdf 3x3swaps.pdf 3x3onebit.pdf
	pdflatex bridges_article
	bibtex bridges_article
	pdflatex bridges_article
	pdflatex bridges_article

3x3table.tex: ../data gen3x3Table.py
	python gen3x3Table.py > $@

3x3scatter.pdf: 3x3.dat 3x3.gnuplot
	gnuplot 3x3.gnuplot

3x3.dat: ../data ../3x3survey/rankings.db gen3x3scatter.py
	python gen3x3scatter.py > $@

3x3correlation.tex: correlationCoefficient.py 3x3.dat
	python correlationCoefficient.py > $@

3x3allcomparisons.dat: comparisons/all_diffs.py 3x3.dat comparisons/hist.py
	python $< | awk '{ print $$3 }' | sed -e 's/\..*//' | sort -nk1 | uniq -c | python comparisons/hist.py > $@

3x3inversions.dat: comparisons/compare_inversions.py 3x3.dat comparisons/hist.py
	python $< | awk '{ print $$3 }' | sed -e 's/\..*//' | sort -nk1 | uniq -c | python comparisons/hist.py > $@ 

3x3inversions.pdf: 3x3inversions.dat 3x3allcomparisons.dat plot_hists.sh
	bash plot_hists.sh "Inversions vs All Comparisons" $@ 3x3inversions.dat inversions

3x3swaps.dat: comparisons/compare_swaps.py 3x3.dat comparisons/hist.py
	python $< | awk '{ print $$3 }' | sed -e 's/\..*//' | sort -nk1 | uniq -c | python comparisons/hist.py > $@

3x3swaps.pdf: 3x3swaps.dat 3x3allcomparisons.dat plot_hists.sh
	bash plot_hists.sh "Swapping X and Y vs All Comparisons" $@ 3x3swaps.dat swaps

3x3onebit.dat: comparisons/compare_onebit.py 3x3.dat comparisons/hist.py
	python $< | awk '{ print $$3 }' | sed -e 's/\..*//' | sort -nk1 | uniq -c | python comparisons/hist.py > $@

3x3onebit.pdf: 3x3onebit.dat 3x3allcomparisons.dat plot_hists.sh
	bash plot_hists.sh "Artworks differing by one pixel vs All Comparisons" $@ 3x3onebit.dat "one pixel differences"

clean:
	rm -f 3x3correlation.tex 3x3.dat 3x3scatter.pdf 3x3table.tex article.aux article.bbl article.blg article.log article.out article.pdf fit.log 3x3allcomparisons.dat 3x3swaps.dat 3x3swaps.pdf 3x3onebit.dat 3x3onebit.pdf 3x3inversions.dat 3x3inversions.pdf
