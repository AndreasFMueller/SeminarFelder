#
# Makefile -- build topology images
#
# (c) 2025 Prof Dr Andreas Müller
#

all:	unterteilung.pdf						\
	sphaere.jpg							\
	morse.pdf							\
	toruspfade.pdf							\
	torushomologie.pdf						\
	rand.pdf

sphaere.png:	sphaere.pov
	povray +A0.1 +W1920 -H1080 -Osphaere.png sphaere.pov

sphaere.jpg:	sphaere.png Makefile
	magick -extract 1080x1080+420+0 sphaere.png sphaere.jpg

unterteilung.pdf:	unterteilung.tex
	pdflatex unterteilung.tex

morse.pdf:	morse.tex torus-morse.jpg torus-levels.jpg
	pdflatex morse.tex

torus-morse.png:	torus-morse.pov torus.inc
	povray +A0.1 -W1920 -H1080 -Otorus-morse.png torus-morse.pov
torus-morse.jpg:	torus-morse.png Makefile
	magick -extract 970x1080+484+0 torus-morse.png torus-morse.jpg

torus-levels.png:	torus-levels.pov torus.inc
	povray +A0.1 -W1920 -H1080 -Otorus-levels.png torus-levels.pov
torus-levels.jpg:	torus-levels.png Makefile
	magick -extract 970x1080+484+0 torus-levels.png torus-levels.jpg

toruspfade.pdf:	toruspfade.tex
	pdflatex toruspfade.tex

torushomologie.pdf:	torushomologie.tex
	pdflatex torushomologie.tex

rand.pdf:	rand.tex randpoints.tex
	pdflatex rand.tex

randpoints.tex:	randpoints.m
	octave randpoints.m
