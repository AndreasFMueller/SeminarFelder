#
# Makefile -- build 3d image
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	vortex.jpg

vortex.png:	vortex.pov
	povray +A0.1 -W1920 -H1080 -Ovortex.png vortex.pov
vortex.jpg:	vortex.png Makefile
	magick -extract 1640x750+18+166 vortex.png vortex.jpg
