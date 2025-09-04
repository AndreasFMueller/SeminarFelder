//
// 3dimage.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

#declare sx = 1.4;
#declare sy = 1.0;
#declare sz = 0.7;

#declare w = 20;

#declare l = 0.8;
#declare Ustart = -0.8;
#declare Uend = 0.8;
#declare Ustep = 0.2;
#declare Vstart = -0.8;
#declare Vend = 0.8;
#declare Vstep = 0.2;
#declare lineradius = 0.007;

#declare meridianbreite = 0.01;

#declare kurvenradius = 0.02;
#declare kurvenfarbe = rgb<0.8,0,0>;
#declare tangentialvektorfarbe = rgb<0.8,0.2,0.8>;
#declare normalenfarbe = rgb<0,0.6,0>;
#declare basisfarbe = rgb<0.2,0.6,1.0>;

place_camera(<53, 30, -40>, <0, sz, 0>, 16/9, 0.0175)
lightsource(<-10, 30, -40>, 10, 0.5 * White)
lightsource(<30, 30, -40>, 10, 0.5 * White)

//arrow(-2*e1, 2*e1, 0.015, White)
//arrow(-(sz+0.3)*e2, (sz+0.3)*e2, 0.015, White)
//arrow(-2*e3, 2*e3, 0.015, White)

arrow( < 0, sz, 0 >, <0, sz + 0.5, 0 >, kurvenradius, normalenfarbe)

sphere { O, 1
	pigment {
		color rgb<0.8,0.8,0.8>
	}
	finish {
		metallic
		specular 0.9
	}
	scale < sx, sz, sy >
}

intersection {
	box { < -2, -sz - 0.4, -1.0>, <2, sz + 0.4, 1.0> }
	plane { < (1/sx) * cos(radians(w)), 0, (1/sy) * sin(radians(w)) >, 0.001 }
	plane { -< (1/sx) * cos(radians(w)), 0, (1/sy) * sin(radians(w)) >, 0.001 }
	pigment {
		color rgbt<0.6,0.8,1.0,0.7>
	}
	finish {
		metallic
		specular 0.9
	}
	no_shadow
}

intersection {
	box { <-l,0, -l>, <l, 2, l> }
	plane { < 0, 1, 0>, sz+0.001 }
	plane { -< 0, 1, 0>, -sz+0.001 }
	pigment {
		color rgbt<0.6,0.8,1.0,0.7>
	}
	finish {
		metallic
		specular 0.9
	}
	no_shadow
	
}

union {
	#declare U = Ustart;
	#while (U < Uend + Ustep/2)
		sphere { < U, sz, Vend >, 0.5 * lineradius }
		sphere { < U, sz, Vstart>, 0.5 * lineradius }
		cylinder { < U, sz, Vstart>, < U, sz, Vend >, 0.5 * lineradius }
		#declare U = U + Ustep;
	#end
	#declare V = Vstart;
	#while (V < Vend + Vstep/2)
		sphere { < Uend, sz, V >, 0.5 * lineradius }
		sphere { < Ustart, sz, V >, 0.5 * lineradius }
		cylinder { < Ustart, sz, V >, < Uend, sz, V >, 0.5 * lineradius }
		#declare V = V + Vstep;
	#end
	pigment {
		color rgb<0.6,0.8,1.0>
	}
	finish {
		metallic
		specular 0.9
	}
	
	no_shadow
}


cylinder { < meridianbreite/2, 0, 0>, <-meridianbreite/2, 0, 0> , 1
	pigment {
		color rgb<0.6,0.4,0.2>
	}
	finish {
		metallic
		specular 0.9
	}
	scale < 1, 1.001 * sz, 1.001 * sy >
}
cylinder { < 0, meridianbreite/2, 0>, < 0, -meridianbreite/2, 0> , 1
	pigment {
		color rgb<0.6,0.4,0.2>
	}
	finish {
		metallic
		specular 0.9
	}
	scale < 1.001 * sx, 1.0 * sz, 1.001 * sy >
}
cylinder { < 0, 0, meridianbreite/2>, < 0, 0, -meridianbreite/2> , 1
	pigment {
		color rgb<0.6,0.4,0.2>
	}
	finish {
		metallic
		specular 0.9
	}
	scale < 1.001 * sx, 1.001 * sz, 1 * sy >
}

#macro schnittkurvenpunkt(phi)
	< sx * sin(phi) * sin(radians(w)), sz * cos(phi), -sy * sin(phi) * cos(radians(w)) >
#end


union {
	#declare phistart = 0;
	#declare phiend = pi;
	#declare phisteps = 50;
	#declare phistep = pi/phisteps;
	#declare phi = phistart;
	#declare p = schnittkurvenpunkt(phi);
	sphere { p, kurvenradius }
	#while (phi < phiend - phistep/2)
		#declare pold = p;
		#declare phi = phi + phistep;
		#declare p = schnittkurvenpunkt(phi);
		sphere { p, kurvenradius }
		sphere { -p, kurvenradius }
		cylinder { pold, p, kurvenradius }
		cylinder { -pold, -p, kurvenradius }
	#end
	pigment {
		color rgb<0.8,0,0>
	}
	finish {
		metallic
		specular 0.9
	}
}

arrow(<0, sz, 0>, <0, sz, 0> + 0.5 * <sx * sin(radians(w)), 0, -cos(radians(w)) >,
	kurvenradius, tangentialvektorfarbe)


#macro F(U, V)
	< U, sz * sqrt(1 - (U/sx) * (U/sx) - (V/sy) * (V/sy)), V >
#end
#macro Ulinie(U)
	#declare vstep = (Vend - Vstart) / 100;
	#declare V = Vstart;
	#declare p = F(U, V);
	sphere { p, lineradius }
	#while (V < Vend - vstep/2)
		#declare pold = p;
		#declare V = V + vstep;
		#declare p = F(U, V);
		sphere { p, lineradius }
		cylinder { pold, p, lineradius }
	#end
#end
#macro Vlinie(V)
	#declare ustep = (Uend - Ustart) / 100;
	#declare U = Ustart;
	#declare p = F(U, V);
	sphere { p, lineradius }
	#while (U < Uend - ustep/2)
		#declare pold = p;
		#declare U = U + ustep;
		#declare p = F(U, V);
		sphere { p, lineradius }
		cylinder { pold, p, lineradius }
	#end
#end

union {
	#declare U = Ustart;
	#while (U < Uend + Ustep/2)
		Ulinie(U)
		#declare U = U + Ustep;
	#end
	#declare V = Vstart;
	#while (V < Vend + Vstep/2)
		Vlinie(V)
		#declare V = V + Vstep;
	#end
	pigment {
		color Yellow
	}
	finish {
		metallic
		specular 0.9
	}
}

arrow( <0, sz, 0>, <0, sz, 0> + <0.5, 0, 0>, kurvenradius, basisfarbe)
arrow( <0, sz, 0>, <0, sz, 0> - <0, 0, 0.5>, kurvenradius, basisfarbe)
