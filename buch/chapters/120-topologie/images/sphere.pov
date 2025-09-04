//
// sphere.pov
//
// (c) 2025 Prof Dr Andreas Müller
//
#include "sphere.inc"

#macro grauekugel()
sphere { <0, 0, 0>, 1
	pigment {
		color kartoffelfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#macro farbigekugel()
intersection {
	box { < -2, cos(radians(30)), -2 >, <2, 2, 2> }
	sphere { <0, 0, 0>, 1 }
	pigment {
		color topfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

intersection {
	box { <-2, -2, -2>, <2, -cos(radians(30)), 2> }
	sphere { <0, 0, 0>, 1 }
	pigment {
		color bottomfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

intersection {
	box { <-2, -cos(radians(30)), -2>, <2, cos(radians(30)), 2> }
	sphere { <0, 0, 0>, 1 }
	pigment {
		color pfadfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

grauekugel()

#macro kugel(theta, phi)
	< cos(phi) * sin(theta), cos(theta), sin(phi) * sin(theta) >
#end

union {
	#declare phistep = pi / 180;
	#declare phimin = 0;
	#declare phimax = radians(360);
	#declare thetastep = radians(10);
	#declare thetamax = radians(170);
	#declare thetamin = thetastep;
	#declare theta = thetamin;
	#while (theta < thetamax + thetastep/2)
		#declare phi = phimin;
		#declare p = kugel(theta, phi);
		#while (phi < phimax - phistep/2)
			#declare pold = p;
			#declare phi = phi + phistep;
			#declare p = kugel(theta, phi);
			cylinder { pold, p, gitterradius }
			sphere { p, gitterradius }
		#end
		#declare theta = theta + thetastep;
	#end
	pigment {
		color kartoffelfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	sphere { kugel(0, 0), pfadradius }
	#declare thetastep = radians(1);
	#declare thetamin = 0;
	#declare thetamax = radians(30);
	#declare phistep = radians(10);
	#declare phimax = radians(360);
	#declare phimin = 0;
	#declare phi = phimin;
	#while (phi < phimax - phistep/2)
		#declare theta = thetamin;
		#declare p = kugel(theta, phi);
		#while (theta < thetamax - thetastep/2)
			#declare pold = p;
			#declare theta = theta + thetastep;
			#declare p = kugel(theta,phi);
			cylinder { pold, p, pfadradius }
			sphere { p, pfadradius }
			cylinder { -pold, -p, pfadradius }
			sphere { -p, pfadradius }
		#end
		#declare phi = phi + phistep;
	#end
	pigment {
		color topfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}


union {
	#declare thetastep = radians(1);
	#declare thetamin = radians(30);
	#declare thetamax = radians(90);
	#declare phistep = radians(10);
	#declare phimax = radians(360);
	#declare phimin = 0;
	#declare phi = phimin;
	#while (phi < phimax - phistep/2)
		#declare theta = thetamin;
		#declare p = kugel(theta, phi);
		#while (theta < thetamax - thetastep/2)
			#declare pold = p;
			#declare theta = theta + thetastep;
			#declare p = kugel(theta,phi);
			cylinder { pold, p, pfadradius }
			sphere { p, pfadradius }
			cylinder { -pold, -p, pfadradius }
			sphere { -p, pfadradius }
		#end
		#declare phi = phi + phistep;
	#end
	pigment {
		color pfadfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}


