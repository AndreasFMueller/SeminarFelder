//
// diffanim.pov -- Differenz zweier Vektoren entlang einer Kurve
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "diffcommon.inc"

tangentialvektor(T1, pfeilfarbe)
tangentialvektor(T2, pfeiltransparent)

#declare T = clock * (T1 - T2) + T2;
pfeiltransportiert(T)

