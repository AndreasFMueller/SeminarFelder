#
# Makefile -- zusammenhang
#
# (c) 2017 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	zusammenhang-handout.pdf MathSem-07-zusammenhang.pdf

include ../slides/Makefile.inc

SOURCES = common.tex slides.tex $(slides)

MathSem-07-zusammenhang.pdf:	MathSem-07-zusammenhang.tex $(SOURCES)
	pdflatex MathSem-07-zusammenhang.tex

zusammenhang-handout.pdf:	zusammenhang-handout.tex $(SOURCES)
	pdflatex zusammenhang-handout.tex

thumbnail:	thumbnail.jpg # fix1.jpg

thumbnail.pdf:	MathSem-07-zusammenhang.pdf
	pdfjam --outfile thumbnail.pdf --papersize '{16cm,9cm}' \
		MathSem-07-zusammenhang.pdf 1
thumbnail.jpg:	thumbnail.pdf
	convert -density 300 thumbnail.pdf \
                -resize 1920x1080 -units PixelsPerInch thumbnail.jpg

fix1.pdf:	MathSem-07-zusammenhang.pdf
	pdfjam --outfile fix1.pdf --papersize '{16cm,9cm}' \
		MathSem-07-zusammenhang.pdf 1
fix1.jpg:	fix1.pdf
	convert -density 300 fix1.pdf \
                -resize 1920x1080 -units PixelsPerInch fix1.jpg

