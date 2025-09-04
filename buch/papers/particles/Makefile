#
# Makefile -- make file for the paper particles
#
# (c) 2020 Prof Dr Andreas Mueller
#

images:
	@echo "no images to be created in particles"

FIGURES := $(wildcard figures/out/*.tex)
PDFS := $(FIGURES:.tex=.pdf)

figures: $(PDFS)
	@echo "All figures built."

figures/out/%.pdf: figures/out/%.tex
	@echo "Compiling $< to $@"
	pdflatex -output-directory=figures/out $<
	@rm -f figures/out/*.log
	
