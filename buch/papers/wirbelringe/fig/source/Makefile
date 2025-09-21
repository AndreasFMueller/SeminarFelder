#
# Makefile
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	wirbelring.png

wirbelring.png:	wirbelring.pov
	pvengine64.exe  -W1920 -H1080 -Owirbelring.png wirbelring.pov //EXIT
wirbelring.jpg:	wirbelring.png Makefile
	magick -extract 1920x920+0+80 wirbelring.png wirbelring.jpg

