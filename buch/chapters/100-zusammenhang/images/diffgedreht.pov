//
// diffgedreht.pov -- Differenz zweier Vektoren entlang einer Kurve
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "diffcommon.inc"

tangentialvektor(T1, pfeilfarbe)
tangentialvektor(T2, pfeiltransparent)

#declare T = T1;
pfeiltransportiert(T)

#declare P1 = kurve(T) + 0.25 * vnormalize(richtung(T));
#declare P2 = kurve(T) + Rgedreht;

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

#declare n = vnormalize(kurve(T1));

#declare west = vnormalize(vcross(n, e2));
#declare upward = vnormalize(vcross(n, west));

arrow(0, 1.1 * west, 0.01, Blue)
arrow(0, 1.1 * upward, 0.01, Green)

#declare w = 0.26;
#declare h = 0.22;

intersection {
        plane { -n, -1.0009 }
        plane { n, 1.0010 }
	plane { west, w }
	plane { -west, w }
	plane { upward, h }
	plane { -upward, h }
        pigment {
                color rgbf<0.6,0.8,0.6,0.7>
        }
        finish {
                metallic
        }
}

