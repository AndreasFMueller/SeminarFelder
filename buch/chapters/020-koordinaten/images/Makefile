#
# Makefile
#
# (c) 2024 Prof Dr Andreas Müller
#
all:	kartpolar.pdf							\
	kartkugel.pdf							\
	koordinaten.pdf							\
	koordinatenwechsel.pdf						\
	kurve.pdf							\
	stereographisch.pdf						\
	stereowechsel.pdf						\
	parallel.pdf

kartpolar.pdf:	kartpolar.tex
	pdflatex kartpolar.tex

kartkugel.png:	kartkugel.pov
	povray +A0.1 -W1920 -H1080 -Okartkugel.png kartkugel.pov

kartkugel.jpg:	kartkugel.png Makefile
	magick -extract 1150x1080+500+0 kartkugel.png kartkugel.jpg

kartkugel.pdf:	kartkugel.tex kartkugel.jpg
	pdflatex kartkugel.tex

koordinaten.pdf:	koordinaten.tex
	pdflatex koordinaten.tex

koordinatenwechsel.pdf:	koordinatenwechsel.tex
	pdflatex koordinatenwechsel.tex

stereowechsel.pdf:	stereowechsel.tex
	pdflatex stereowechsel.tex

stereographisch.png:	stereographisch.pov
	povray +A0.1 -W1920 -H1080 -Ostereographisch.png stereographisch.pov

stereographisch.jpg:	stereographisch.png Makefile
	magick -extract 1870x1080+50+0 stereographisch.png stereographisch.jpg

stereographisch.pdf:	stereographisch.tex stereographisch.jpg
	pdflatex stereographisch.tex

kurve.pdf:	kurve.tex kurve.jpg
	pdflatex kurve.tex

kurve.png:	kurve.pov
	povray +A0.1 -W1920 -H1080 -Okurve.png kurve.pov
kurve.jpg:	kurve.png Makefile
	magick -extract 1744x1080+118+0 kurve.png kurve.jpg

parallel.png:	parallel.pov
	povray +A0.1 -W1920 -H1080 -Oparallel.png parallel.pov

parallel.jpg:	parallel.png Makefile
	magick -extract 1052x1080+320+0 parallel.png parallel.jpg

parallel.pdf:	parallel.tex parallel.jpg
	pdflatex parallel.tex

tangentialvektoren.png:	tangentialvektoren.pov tangentialvektoren.inc
	povray +A0.1 -W1920 -H1080 -Otangentialvektoren.png \
		tangentialvektoren.pov

tangentialvektoren.inc:	tangentialvektoren.m
	octave tangentialvektoren.m

tangentialvektoren.jpg:	tangentialvektoren.png Makefile
	magick -extract 1250x1080+336+0 tangentialvektoren.png \
		tangentialvektoren.jpg
