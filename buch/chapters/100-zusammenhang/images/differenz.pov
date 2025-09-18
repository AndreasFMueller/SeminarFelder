//
// differenz.pov -- Differenz zweier Vektoren entlang einer Kurve
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "diffcommon.inc"

tangentialvektor(T1, pfeilfarbe)
tangentialvektor(T2, pfeilfarbe)

//#declare T = 0;
//pfeiltransportiert(T)

#declare P1 = kurve(T1) + 0.25 * vnormalize(richtung(T1));
#declare P2 = kurve(T2) + 0.25 * vnormalize(richtung(T2));
union {
	cylinder { P1, P2, 0.003 }
	sphere { P1, 0.003 }
	sphere { P2, 0.003 }
	pigment {
		color Red
	}
	finish {
		metallic
		specular 0.9
	}
}

