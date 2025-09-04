//
// sphere.pov -- distorted sphere
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

place_camera(<-33, 20, 50>, <0, 0, 0>, 16/9, 0.04)
lightsource(<10, 5, 40>, 1, White)

arrow(-e1, e1, 0.01, White)
arrow(-e2, e2, 0.01, White)
arrow(-e3, e3, 0.01, White)

#include "sphere.inc"

mesh {
	gitter()
	pigment {
		color rgb<0.8,0.8,0.8>
	}
	finish {
		metallic
		specular 0.9
	}
}
