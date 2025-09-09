//
// 2simplex.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

#declare s = (e1 + e2 + e3) / 3;

place_camera(<33, 20, 50>, s + <0,0.247,0> , 16/9, 0.0234)
lightsource(<40, 35, -10>, 1, White)

arrow(-0.3 * e1, 1.2 * e1, 0.01, White)
arrow(-0.3 * e2, 1.2 * e2, 0.01, White)
arrow(-0.3 * e3, 1.2 * e3, 0.01, White)

#declare simplexfarbe = rgb<0.2,0.6,1.0>;
#declare simplexfarbet = rgbt<0.2,0.6,1.0,0.2>;
#declare simplexradius = 0.014;
#declare punktfarbe = rgb<0.8,0.4,0.6>;

triangle { e1, e2, e3 
	pigment {
		color simplexfarbet
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	cylinder { e1, e2, simplexradius }
	cylinder { e1, e3, simplexradius }
	cylinder { e2, e3, simplexradius }
	sphere { e1, 2 * simplexradius }
	sphere { e2, 2 * simplexradius }
	sphere { e3, 2 * simplexradius }
	pigment {
		color simplexfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare t1 = 0.35;
#declare t2 = 0.2;
#declare h = 1 - t1 - t2;
sphere { <t1, h, t2>, 2 * simplexradius
	pigment {
		color punktfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare lineradius = 0.007;

union {
	cylinder { < t1,  0, t2 >, < t1,  h, t2 >, lineradius }
	cylinder { < t1,  0, t2 >, < t1,  0, 0  >, lineradius }
	cylinder { < t1,  0, t2 >, <  0,  0, t2 >, lineradius }
	sphere { < t1, 0, t2 >, lineradius }
	pigment {
		color punktfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare Xstep = 0.1;
#declare Xmax = 1.1;
#declare Xmin = -0.2;
#macro tick(X)
	cylinder {
		< (X - 0.003), 0, 0 >,
		< (X + 0.003), 0, 0 >,
		0.015
	}
	cylinder {
		< 0, (X - 0.003), 0 >,
		< 0, (X + 0.003), 0 >,
		0.015
	}
	cylinder {
		< 0, 0, (X - 0.003) >,
		< 0, 0, (X + 0.003) >,
		0.015
	}
#end
union {
	#declare X = 0.1;
	#while (X < Xmax + Xstep/2)
		tick(X)
		#declare X = X + Xstep;
	#end
	#declare X = -0.1;
	#while (X > Xmin - Xstep/2)
		tick(X)
		#declare X = X - Xstep;
	#end
	
	pigment {
		color White
	}
	finish {
		metallic
		specular 0.9
	}
}
