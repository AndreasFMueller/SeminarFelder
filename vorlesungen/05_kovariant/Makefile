#
# Makefile -- kovariant
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	kovariant-handout.pdf MathSem-05-kovariant.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-05-kovariant.pdf:	MathSem-05-kovariant.tex $(SOURCES)
	pdflatex MathSem-05-kovariant.tex

kovariant-handout.pdf:	kovariant-handout.tex $(SOURCES)
	pdflatex kovariant-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-05-kovariant.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-05-kovariant.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-05-kovariant.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-05-kovariant.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

