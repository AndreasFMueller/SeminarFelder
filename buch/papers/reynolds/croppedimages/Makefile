#
# Makefile -- create cropped images
#
# (c) 2025 Prof Dr Andreas Müller
#
modelle = dns.png k-e.png k-w.png sst.png

felder = 								\
	eddy-viscosity.png						\
	turbulence-kinetic-energy.png					\
	turbulent-viscosity.png

all: $(modelle) $(felder)

ausschnitt1=2504x1858+0+0
ausschnitt1=2278x762+87+548

dns.png: ../images/dns.png Makefile
	magick -extract $(ausschnitt1) ../images/dns.png dns.png

ausschnitt2=2156x720+148+568

k-e.png: ../images/k-e.png Makefile
	magick -extract $(ausschnitt2) ../images/k-e.png k-e.png

k-w.png: ../images/k-w.png Makefile
	magick -extract $(ausschnitt2) ../images/k-w.png k-w.png

sst.png: ../images/sst.png Makefile
	magick -extract $(ausschnitt2) ../images/sst.png sst.png

eddy-viscosity.png: ../images/eddy-viscosity.png Makefile
	magick ../images/eddy-viscosity.png \
		\( -clone 0 -crop 1450x484+384+382 +repage -write mpr:patch +delete \) \
		-region 1450x484+384+382 -fill white -colorize 100% +region \
		mpr:patch -geometry +334+152 -compose over -composite \
		-crop 1782x700+2+40 \
		eddy-viscosity.png

turbulence-kinetic-energy.png: ../images/turbulence-kinetic-energy.png Makefile
	magick ../images/turbulence-kinetic-energy.png \
		\( -clone 0 -crop 1450x484+384+382 +repage -write mpr:patch +delete \) \
		-region 1450x484+384+382 -fill white -colorize 100% +region \
		mpr:patch -geometry +334+152 -compose over -composite \
		-crop 1782x700+2+40 \
		turbulence-kinetic-energy.png

turbulent-viscosity.png: ../images/turbulent-viscosity.png Makefile
	magick ../images/turbulent-viscosity.png \
		\( -clone 0 -crop 1450x484+384+382 +repage -write mpr:patch +delete \) \
		-region 1450x484+384+382 -fill white -colorize 100% +region \
		mpr:patch -geometry +334+152 -compose over -composite \
		-crop 1782x700+2+40 \
		turbulent-viscosity.png

x.png:	../images/eddy-viscosity.png Makefile
	magick ../images/eddy-viscosity.png \
		\( -clone 0 -crop 1450x484+384+382 +repage -write mpr:patch +delete \) \
		-region 1450x484+384+382 -fill white -colorize 100% +region \
		mpr:patch -geometry +334+152 -compose over -composite \
		-crop 1782x700+2+40 \
		x.png

