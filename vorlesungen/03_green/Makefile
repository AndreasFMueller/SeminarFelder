#
# Makefile -- green
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	green-handout.pdf MathSem-03-green.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-03-green.pdf:	MathSem-03-green.tex $(SOURCES)
	pdflatex MathSem-03-green.tex

green-handout.pdf:	green-handout.tex $(SOURCES)
	pdflatex green-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-03-green.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-03-green.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-03-green.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-03-green.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

