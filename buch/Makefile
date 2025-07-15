#
# Makefile zum Skript ueber Felder
#
# (c) 2022 Prof Dr Andreas Mueller, OST Ostschweizer Fachhochschule
#
seminar = SeminarFelder

all:	buch.pdf

buch:	$(seminar).pdf

papers/common/Makefile.inc:	papers/common/paperlist

include common/Makefile.inc
include chapters/Makefile.inc
include papers/common/Makefile.inc
include papers/common/includes.inc

ALLTEXFILES = $(TEXFILES) $(CHAPTERFILES)

#
# Buchblock für Druckerei
#
$(workdir):
	mkdir -p $(workdir)
buch.pdf:	$(workdir)/buch.pdf
	cp $(workdir)/buch.pdf buch.pdf

$(workdir)/buch.pdf:	$(workdir) buch.tex $(TEXFILES) $(workdir)/buch.ind $(BLXFILES)
	$(pdflatex) buch.tex
	cd $(workdir); $(bibtex) buch

$(workdir)/buch.ind:	$(workdir) $(workdir)/buch.idx
	cd $(workdir); $(makeindex) buch.idx

$(workdir)/buch.idx:	$(workdir) buch.tex $(TEXFILES) images
	$(touch) $(workdir)/buch.ind
	$(pdflatex) buch.tex

#
# Papers in einzelne PDF-Files separieren für digitales Feedback
#
separate:	build/buch.aux buch.pdf
	bash tools/splitpapers

#
# Version mit Buchdeckeln für Release/Website
#
buch = $(seminar)
$(buch).pdf:	$(workdir)/$(buch).pdf
	cp $(workdir)/$(buch).pdf $(buch).pdf

$(workdir)/$(seminar).pdf:	$(buch).tex $(TEXFILES) $(workdir)/$(buch).ind $(SBLXFILES)
	$(pdflatex) $(buch).tex
	cd $(workdir); $(bibtex) $(buch)

$(workdir)/$(buch).idx:	$(workdir) $(buch).tex $(TEXFILES) images
	$(touch) $(workdir)/$(buch).ind
	$(pdflatex) $(buch).tex

$(workdir)/$(buch).ind:	$(workdir)/$(buch).idx
	cd $(workdir); $(makeindex) $(buch).idx

##
## Einzelnes Kapitel/Paper
##
include common/Makefile-paper.inc
include common/Makefile-chapter.inc

#
# This Makefile can also construct the short tests
#
include test/Makefile.inc

#
# Errata
#
errata.pdf:	errata.tex
	$(pdflatex) errata.tex

#
# publish
#
publish:	$(seminar).pdf
	bash publish
