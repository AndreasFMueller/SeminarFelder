#
# Makefile -- gravitation
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	gravitation-handout.pdf MathSem-08-gravitation.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-08-gravitation.pdf:	MathSem-08-gravitation.tex $(SOURCES)
	pdflatex MathSem-08-gravitation.tex

gravitation-handout.pdf:	gravitation-handout.tex $(SOURCES)
	pdflatex gravitation-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-08-gravitation.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-08-gravitation.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-08-gravitation.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-08-gravitation.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

