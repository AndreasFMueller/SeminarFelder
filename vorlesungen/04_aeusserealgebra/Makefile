#
# Makefile -- aeusserealgebra
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	aeusserealgebra-handout.pdf MathSem-04-aeusserealgebra.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-04-aeusserealgebra.pdf:	MathSem-04-aeusserealgebra.tex $(SOURCES)
	pdflatex MathSem-04-aeusserealgebra.tex

aeusserealgebra-handout.pdf:	aeusserealgebra-handout.tex $(SOURCES)
	pdflatex aeusserealgebra-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-04-aeusserealgebra.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-04-aeusserealgebra.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-04-aeusserealgebra.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-04-aeusserealgebra.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

