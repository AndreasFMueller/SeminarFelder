#
# Makefile -- qft
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	qft-handout.pdf MathSem-07-qft.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-07-qft.pdf:	MathSem-07-qft.tex $(SOURCES)
	pdflatex MathSem-07-qft.tex

qft-handout.pdf:	qft-handout.tex $(SOURCES)
	pdflatex qft-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-07-qft.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-07-qft.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-07-qft.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-07-qft.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

