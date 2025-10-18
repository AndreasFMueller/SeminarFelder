#
# Makefile -- build the book cover
#
# (c) 2018 Prof Dr Andreas Müller, Hochschule Rapperswil
#
all:	buchcover.jpg backcover.jpg front.pdf back.pdf

buchcover.pdf:	buchcover.tex teilnehmer.tex ruecken1.png
	pdflatex buchcover.tex

buchcover.png:	buchcover.pdf Makefile 
	magick -density 300 -extract 2054x2900+2740+190 buchcover.pdf \
		buchcover.png
buchcover.jpg:	buchcover.png
	magick buchcover.png buchcover.jpg
buchcover-small.jpg:	buchcover.jpg
	magick buchcover.jpg -scale 50% buchcover-small.jpg
backcover.png:	buchcover.pdf Makefile
	magick -density 300 -extract 2054x2900+192+190 buchcover.pdf \
		backcover.png
backcover.jpg:	backcover.png
	magick backcover.png backcover.jpg

front.pdf:	front.tex buchcover.pdf
	pdflatex front.tex
front.jpg:	front.pdf
	magick -density 150 front.pdf front.jpg

back.pdf:	back.tex buchcover.pdf
	pdflatex back.tex
back.jpg:	back.pdf
	magick -density 150 back.pdf back.jpg

ruecken1.pdf:	ruecken1.tex
	pdflatex ruecken1.tex

ruecken2.pdf:	ruecken2.tex
	pdflatex ruecken2.tex

ruecken2.png:	ruecken2.pdf Makefile
	magick -density 300 ruecken2.pdf -alpha set -background none \
		-channel A -sparse-color barycentric "0,0 none %[w],0 white" \
		+channel ruecken2.png
ruecken1.png:	ruecken1.pdf ruecken2.png Makefile
	magick -density 300 ruecken1.pdf ruecken2.png -composite ruecken1.png

