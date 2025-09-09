//
// zyklus.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "tetra.inc"
#include "zyklusgitter.inc"

#declare dunkelgruent = rgbt<0.2,0.6,0.2,0.4>;
#declare dunkelgruen = rgb<0.2,0.6,0.2>;

union {
	//sphere { A, knotenradius }
	//sphere { B, knotenradius }
	//sphere { C, knotenradius }
	//sphere { D, knotenradius }
	sphere { S, 2 * knotenradius }
	pigment {
		color dunkelgruen
	}
	finish {
		metallic
		specular 0.9
	}
}


union {
	dreieck(A, B, S, dunkelgruent)
	dreieck(A, C, S, dunkelgruent)
	dreieck(A, D, S, dunkelgruent)
	dreieck(B, C, S, dunkelgruent)
	dreieck(B, D, S, dunkelgruent)
	dreieck(C, D, S, dunkelgruent)
	no_shadow
}

gitter()
tetraeder()
