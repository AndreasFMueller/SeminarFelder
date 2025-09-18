//
// tetra.inc
//
// (c) 2025 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"
#include "tetrapoints.inc"

#declare A = A_2_4_2;
#declare B = A_2_3_2;
#declare C = A_2_3_3;
#declare D = A_1_4_2;
#declare S = 0.2 * D + 0.2 * A + 0.2 * B + 0.4 * C;
#declare S1 = (A + B + D + S) / 4;

place_camera(<-33, 20, 50>, S, 16/9, 0.025)
lightsource(<-40, 15, 40>, 10, White)

#declare gitterfarbe = rgb<0.8,0.8,0.8>;
#declare zyklusfarbe = rgb<0.8,0.6,0.8>;
#declare kantenradius = 0.008;
#declare knotenradius = 2 * kantenradius;

//arrow(-e1, e1, 0.01, White)
//arrow(-e2, e2, 0.01, White)
//arrow(-e3, e3, 0.01, White)

#macro knoten(A, farbe)
	sphere { A, knotenradius
		pigment {
			color farbe
		}
		finish {
			metallic
			specular 0.9
		}
	}
#end

#macro kante(A, B, farbe)
cylinder { A, B, kantenradius
	pigment {
		color farbe
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#macro dreieck(A, B, C, farbe)
	mesh {
		triangle { A, B, C }
		pigment {
			color farbe
		}
		finish {
			metallic
			specular 0.9
		}
	}
#end
