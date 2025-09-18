//
// 3dimage.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

#declare kamerarichtung = <53, 0, -20>;
#declare kamerahoehe = 20;

place_camera(kamerarichtung + <0, kamerahoehe, 0>, <0, 0, 0>, 16/9, 0.048)
lightsource(<20, 5, -40>, 10, White)

//arrow(-e1, e1, 0.01, White)
//arrow(-e2, e2, 0.01, White)
//arrow(-e3, e3, 0.01, White)

#macro zylinder(R)
object {
	cylinder { <0, -0.06/(R*R), 0>, <0, 0.06/(R*R), 0>, R }
	pigment {
		color rgbt<0.8,0.8,0.8,0.5>
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#declare sektorwinkel = radians(-30);

#declare wirbelradius = 0.03;

#macro vortex(h, r)
union {
	difference {
		torus { r, wirbelradius
			translate <0, h, 0>
		}
		intersection {
			plane { -< 0, 0, 1 >, 0 }
			plane { -< cos(sektorwinkel), 0, sin(sektorwinkel) >, 0 }
		}
	}
	cone { < r, h, 0 >, 2 * wirbelradius, < r, h, 4 * wirbelradius >, 0 }
	pigment {
		color rgb<0.6,0.8,1.0>
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#declare offsetrichtung = vnormalize(vcross(<0,1,0>, kamerarichtung));

#declare zylinderradius = 0.4;

zylinder(zylinderradius)
vortex(0.1, 1.3 * zylinderradius)
vortex(-0.1, 1.3 * zylinderradius)

#declare zylinderradius = 0.6;
union {
	zylinder(zylinderradius)
	vortex(0, 1.3 * zylinderradius)
	translate 1.7 * offsetrichtung
}

#declare zylinderradius = 0.25;
union {
	zylinder(zylinderradius)
	vortex(0.2, 1.3 * zylinderradius)
	vortex(0, 1.3 * zylinderradius)
	vortex(-0.2, 1.3 * zylinderradius)
	translate -1.5 * offsetrichtung
}
