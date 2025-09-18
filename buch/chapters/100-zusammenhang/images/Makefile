#
# Makefile
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	differenz.pdf							\
	kugeldreieck.pdf						\
	polargeodaete.pdf						\
	transport.pdf

#
# Kugeldreieck
#
kugeldreieck.png:	kugeldreieck.pov
	povray +A0.1 -W1920 -H1080 -Okugeldreieck.png kugeldreieck.pov

kugeldreieck.jpg:	kugeldreieck.png Makefile
	magick -extract 1300x1080+310+0 kugeldreieck.png kugeldreieck.jpg

kugeldreieck.pdf:	kugeldreieck.tex kugeldreieck.jpg
	pdflatex kugeldreieck.tex

#
# Geodäte in Polarkoordinaten
#
polargeodaete.pdf:	polargeodaete.tex
	pdflatex polargeodaete.tex

#
# Transport entlang einer Kurve
#
transport.png:	transport.pov transportvektoren.inc
	povray +A0.1 -W1920 -H1080 -Otransport.png transport.pov

transport.jpg:	transport.png Makefile
	magick -extract 1420x1080+250+0 transport.png transport.jpg

transportvektoren.inc:	transport.m
	octave transport.m

transport.pdf:	transport.tex transport.jpg
	pdflatex transport.tex

#
# Differenz
#
differenz.png:	differenz.pov diffcommon.inc
	povray +A0.1 -W1920 -H1080 -Odifferenz.png differenz.pov
diffgedreht.png:	diffgedreht.pov diffcommon.inc
	povray +A0.1 -W1920 -H1080 -Odiffgedreht.png diffgedreht.pov

differenz.jpg:	differenz.png
	magick differenz.png differenz.jpg
diffgedreht.jpg:	diffgedreht.png
	magick diffgedreht.png diffgedreht.jpg

differenz.pdf:	differenz.tex differenz.jpg diffgedreht.jpg
	pdflatex differenz.tex

#
# Animation
#
diffanim.timestamp:	diffanim.pov diffanim.ini diffcommon.inc
	povray +A0.1 -W1920 -H1080 -Odiffanim/d.png diffanim.ini
	touch diffanim.timestamp

diffjpgdir = ../../../../vorlesungen/slides/7
diffanimjpg:	diffanim.timestamp diffgedreht.jpg differenz.jpg
	for f in diffanim/*.png; 					\
	do 								\
		magick $${f} $(diffjpgdir)/`basename $$f .png`.jpg ;	\
	done
	cp diffgedreht.jpg $(diffjpgdir)
	cp differenz.jpg $(diffjpgdir)
