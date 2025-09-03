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
	rand.pdf							\
	unterzyklen.pdf							\
	zyklus.pdf							\
	simplex.pdf

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

unterzyklen.pdf:	unterzyklen.tex u.tex
	pdflatex unterzyklen.tex

u.tex:	u.m
	octave u.m

zyklusgroesse = 1020x1080+450+0

zhomolog.png:	zhomolog.pov tetra.inc tetrapoints.inc zyklusgitter.inc
	povray +A0.1 -W1920 -H1080 -Ozhomolog.png zhomolog.pov
zhomolog.jpg:	zhomolog.png Makefile
	magick -extract $(zyklusgroesse) zhomolog.png zhomolog.jpg

zyklus.png:	zyklus.pov tetra.inc tetrapoints.inc zyklusgitter.inc
	povray +A0.1 -W1920 -H1080 -Ozyklus.png zyklus.pov
zyklus.jpg:	zyklus.png Makefile
	magick -extract $(zyklusgroesse) zyklus.png zyklus.jpg

tetrapoints.inc:	tetra.m
	octave tetra.m

zyklus.pdf:	zyklus.tex zhomolog.jpg zyklus.jpg
	pdflatex zyklus.tex

2simplex.png:	2simplex.pov
	povray +A0.1 -W1920 -H1080 -O2simplex.png 2simplex.pov
2simplex.jpg:	2simplex.png Makefile
	magick -extract 1234x1080+288+0 2simplex.png 2simplex.jpg
simplex.pdf:	simplex.tex 2simplex.jpg
	pdflatex simplex.tex
