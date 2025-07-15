#
# Einzelnes Paper
#
chapter:	chapter.pdf

chapter.pdf:	$(workdir) $(workdir)/chapter.pdf
	cp $(workdir)/chapter.pdf .

$(workdir)/chapter.pdf:	chapter.tex common/chaptername.tex $(workdir)/chapter.ind $(TEXFILES) $(workdir)/chapter1-blx.bbl
	$(pdflatex) chapter.tex
	cd $(workdir); $(bibtex) chapter

$(workdir)/chapter1-blx.bbl:       $(workdir)/chapter1-blx.aux
	cd $(workdir); bibtex chapter1-blx

$(workdir)/chapter.ind:	$(workdir) $(workdir)/chapter.idx
	cd $(workdir); $(makeindex) chapter.idx

$(workdir)/chapter.idx:	$(workdir) chapter.tex $(TEXFILES) images
	$(touch) $(workdir)/chapter.ind
	$(pdflatex) chapter.tex

common/chaptername.tex:
	@echo "FEHLER: Das File chaptername.tex wurde nicht gefunden."
	@exit 1

