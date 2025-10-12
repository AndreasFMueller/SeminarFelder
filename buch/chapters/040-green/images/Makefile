#
# Makefile
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	parallelogramm.pdf						\
	lorentz.pdf							\
	randkarten.pdf							\
	homotopie.pdf							\
	volint.pdf							\
	greenbeweis.pdf							\
	greenrand.pdf							\
	greenrand2d.pdf							\
	band.pdf							\
	moebius.pdf							\
	quader.pdf

#
# Parallelogramm-Fäche
#
parallelogramm.pdf:	parallelogramm.tex
	pdflatex parallelogramm.tex

#
# Lorentz-Kraft
#
lorentz.png:	lorentz.pov
	povray +A0.1 -W1920 -H1080 -Olorentz.png lorentz.pov

lorentz.jpg:	lorentz.png Makefile
	magick -extract 920x1080+420+0 lorentz.png lorentz.jpg

lorentz.pdf:	lorentz.tex lorentz.jpg
	pdflatex lorentz.tex

#
# Randkarten
#
randkarten.png:	randkarten.pov	
	povray +A0.1 -W1920 -H1080 -Orandkarten.png randkarten.pov

randkarten.jpg:	randkarten.png Makefile
	magick -extract 1574x1040+173+12 randkarten.png randkarten.jpg

randkarten.pdf:	randkarten.tex randkarten.jpg
	pdflatex randkarten.tex

#
# Homotopie
#
homotopie.png:	homotopie.pov
	povray +A0.1 -W1920 -H1080 -Ohomotopie.png homotopie.pov

homotopie.jpg:	homotopie.png Makefile
	magick -extract 1820x1050+4+2 homotopie.png homotopie.jpg

homotopie.pdf:	homotopie.tex homotopie.jpg
	pdflatex homotopie.tex

#
# Integral
#
volintx.png:	volintx.pov volintcommon.inc volintdata.inc
	povray +A0.1 -W1920 -H1080 -Ovolintx.png volintx.pov 

volintx.jpg:	volintx.png
	magick volintx.png volintx.jpg

volinty.png:	volinty.pov volintcommon.inc volintdata.inc
	povray +A0.1 -W1920 -H1080 -Ovolinty.png volinty.pov 

volinty.jpg:	volinty.png
	magick volinty.png volinty.jpg

volintdata.inc:	volint.m
	octave volint.m

volint.pdf:	volint.tex volintx.jpg volinty.jpg
	pdflatex volint.tex

#
# greenrand
#
green = greenrand.inc greenranddata.inc
greengeometry = 1680x492+230+318

greenrandgerade.png:	greenrandgerade.pov $(green)
	povray +A0.1 -W1920 -H1080 -Ogreenrandgerade.png greenrandgerade.pov

greenrandgerade.jpg:	greenrandgerade.png Makefile
	magick -extract $(greengeometry) greenrandgerade.png greenrandgerade.jpg

greenrandgekruemmt.png:	greenrandgekruemmt.pov $(green)
	povray +A0.1 -W1920 -H1080 -Ogreenrandgekruemmt.png \
		greenrandgekruemmt.pov

greenrandgekruemmt.jpg:	greenrandgekruemmt.png Makefile
	magick -extract $(greengeometry) greenrandgekruemmt.png \
		greenrandgekruemmt.jpg

greenranddata.inc:	greenrand.m
	octave greenrand.m

greenrand.pdf:	greenrand.tex greenrandgerade.jpg greenrandgekruemmt.jpg
	pdflatex greenrand.tex

#
# greenrand2d
#
greenrand2d.pdf:	greenrand2d.tex
	pdflatex greenrand2d.tex

#
# Green Beweis
#
greenbeweis.pdf:        greenbeweis.tex
	pdflatex greenbeweis.tex

band.pdf:	band.tex band.jpg
	pdflatex band.tex

band.png:	band.pov
	povray +A0.1 -W1920 -H1080 -Oband.png band.pov
band.jpg:	band.png
	magick band.png band.jpg


moebius.png:	moebius.pov
	povray +A0.1 -W1920 -H1080 -Omoebius.png moebius.pov
moebius.jpg:	moebius.png Makefile
	magick -extract 1882x710+20+104 moebius.png moebius.jpg
moebius.pdf:	moebius.tex moebius.jpg
	pdflatex moebius.tex

quader.pdf:	quader.tex
	pdflatex quader.tex

