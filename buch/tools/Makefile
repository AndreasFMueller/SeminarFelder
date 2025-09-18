#
# Makefile
#
# (c) 2025 Prof Dr Andreas Müller
#
all:	farbseiten

chapters:	chapters.c
	gcc -o chapters -Wall -g -O2 chapters.c

test:	chapters
	./chapters --debug --auxfile ../build/buch.aux --numbers --pages --chapters << /dev/null

farbseiten:	chapters farbseiten.sh
	bash farbseiten.sh
