#
# Einzelnes Paper
#
paper:	paper.pdf

paper.pdf:	$(workdir) $(workdir)/paper.pdf
	cp $(workdir)/paper.pdf .

$(workdir)/paper.pdf:	paper.tex papername.tex $(workdir)/paper.ind $(TEXFILES) $(workdir)/paper1-blx.bbl
	$(pdflatex) paper.tex
	cd $(workdir); $(bibtex) paper

$(workdir)/paper1-blx.bbl:       $(workdir)/paper1-blx.aux
	cd $(workdir); bibtex paper1-blx

$(workdir)/paper.ind:	$(workdir) $(workdir)/paper.idx
	cd $(workdir); $(makeindex) paper.idx

$(workdir)/paper.idx:	$(workdir) paper.tex $(TEXFILES) images
	$(touch) $(workdir)/paper.ind
	$(pdflatex) paper.tex


papername.tex:
	@echo "FEHLER: Das File papername.tex wurde nicht gefunden. Es muss von Hand "
	@echo "FEHLER: angelegt werden. Es enthält den Namen des Kapitels, das vom "
	@echo "FEHLER: File paper.tex als einzelnes Kapitel gesetzt werden soll. "
	@echo "FEHLER: Der Name muss in der Form"
	@echo "FEHLER: "
	@echo "FEHLER: \\def\\papername{diffortho}"
	@echo "FEHLER: "
	@echo "FEHLER: eingegeben werden, damit das Paper 'diffortho' gebaut wird."
	@echo "FEHLER: Konsultieren Sie die Anleitung zum Seminar, Abschnitt 4.2,"
	@echo "FEHLER: für Details."
	@echo "FEHLER: Achtung: Ihr persöhnliches papername.tex darf nicht zum "
	@echo "FEHLER:          Repo hinzugefügt werden!"
	@exit 1

