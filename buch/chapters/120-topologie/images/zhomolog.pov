//
// zhomolog.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "tetra.inc"
#include "zyklusgitter.inc"

#declare dunkelgruent = rgbt<0.2,0.6,0.2,0.4>;
#declare dunkelgruen = rgb<0.2,0.6,0.2>;

#declare T = 0.90;
#declare Aa = T * A + (1 - T) * S1;
#declare Bb = T * B + (1 - T) * S1;
#declare Dd = T * D + (1 - T) * S1;
#declare Ss = T * S + (1 - T) * S1;

mesh {
	triangle { Aa, Bb, Dd }
	triangle { Aa, Bb, Ss }
	triangle { Aa, Dd, Ss }
	triangle { Dd, Bb, Ss }
	pigment {
		color rgbt<0.8,0.2,0.2,0.5>
	}
	finish {
		metallic
		specular 0.9
	}
}

triangle { A, B, D
	pigment {
		color rgbt<0.2,0.6,1.0>
	}
	finish {
		metallic
		specular 0.9
	}
	translate < 0, 0.0001, 0 >
}

gitter()
tetraeder()
