#
# Makefile -- build felder.tex poster
#
# (c) 2015 Prof Dr Andreas Mueller, Hochschule Rapperswil
#
seminar = felder

$(seminar).pdf:	$(seminar).tex ../cover/buchcover.png qrcode.pdf
	pdflatex $(seminar).tex

qrcode.pdf:     qrcode.tex ../cover/mathman.png
	pdflatex qrcode.tex

