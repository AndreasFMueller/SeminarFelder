#
# Makefile -- build images
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	polar.pdf bipolar.pdf

polar.pdf:	polar.tex
	pdflatex polar.tex

bipolar.pdf:	bipolar.tex bipolarpaths.tex
	pdflatex bipolar.tex

bipolarpaths.tex:	bipolar.m
	octave bipolar.m

