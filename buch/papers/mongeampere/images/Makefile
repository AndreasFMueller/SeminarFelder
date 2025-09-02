#
# Makefile -- build images
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	schnittkurven.pdf

schnittkurven.pdf:	schnittkurven.tex schnittkurven.jpg
	pdflatex schnittkurven.tex

schnittkurven.png:	schnittkurven.pov
	povray +A0.1 -W1920 -H1080 -Oschnittkurven.png schnittkurven.pov

schnittkurven.jpg:	schnittkurven.png
	magick -extract 1920x1080+0+0 schnittkurven.png schnittkurven.jpg

