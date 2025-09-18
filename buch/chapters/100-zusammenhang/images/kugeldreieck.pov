//
// kugeldreieck.pov -- Kugeldreieck zur Parametrisierung
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

#declare O = <0, 0, 0>;
#declare longitude = radians(80);
#declare beta = radians(30);
#declare dreieck = rgb<0.95,0.95,0.95>;
#declare kugelfarbe = rgb<0.5,0.5,0.5>;
#declare winkel = rgb<1.0,0.6,0.2>;
#declare aequatorfarbe = rgb<0.2,0.6,1.0>;
#declare aequatorwinkel = rgb<0.2,0.6,1.0>;
#declare meridianfarbe = rgb<0.2,0.8,0.4>;
#declare meridianwinkel = rgb<0.2,0.8,0.4>;
#declare grosskreisfarbe = rgb<0.8,0.4,0.6>;
#declare grosskreiswinkel = rgb<0.8,0.4,0.6>;
#declare d = 0.005;

#declare B = < cos(longitude) * cos(beta), sin(beta), sin(longitude) * cos(beta) >;

place_camera(<33, 20, 50>, <0, 0.32, 0>, 16/9, 0.027)
lightsource(<40, 50, 10>, 1, White)

arrow(-1.2 * e1, 1.2 * e1, 0.01, White)
arrow(-1.2 * e2, 1.2 * e2, 0.01, White)
arrow(-1.2 * e3, 1.2 * e3, 0.01, White)

sphere { O, 1
	pigment {
		color kugelfarbe
	}
	finish {
		metallic
		specular 0.5
	}
}

#macro axis(s)
< -sin(longitude-s), 0, cos(longitude-s) >
#end

intersection {
	sphere { O, 1.001 }
	plane { -e2, 0 }
	plane { axis(0), 0 }
	plane { < 0, cos(beta), -sin(beta) >, 0 }
	pigment {
		color dreieck
	}
	finish {
		metallic
		specular 0.99
	}
}

intersection {
	cylinder { <0,-0.002, 0>, <0, 0.002, 0>, 1.1 }
	plane { -e3, 0 }
	plane { axis(0), 0 }
	pigment {
		color winkel
	}
	finish {
		metallic
		specular 0.99
	}
}


intersection {
	cylinder { 0.002 * axis(0), -0.002 * axis(0), 1.1 }
	plane { -e3, 0 }
	plane { -< 0, cos(beta), -sin(beta) >, 0 }
	pigment {
		color winkel
	}
	finish {
		metallic
		specular 0.99
	}
}

#declare s = radians(8);

intersection {
	sphere { O, 1 + d }
	plane { -e2, 0 }
	plane { axis(0), 0 }
	plane { -axis(s), 0 }
	plane { < 0, cos(s), -sin(s) >, 0 }
	pigment {
		color grosskreiswinkel
	}
	finish {
		metallic
		specular 0.99
	}
}

intersection {
	sphere { O, 1 + d }
	cone { O, 0, 1.1 * e1, 0.25 }
	plane { -e2, 0 }
	plane { < 0, cos(beta), -sin(beta) >, 0 }
	pigment {
		color meridianwinkel
	}
	finish {
		metallic
		specular 0.99
	}
}

intersection {
	sphere { O, 1 + d }
	cone { O, 0, 1.1 * B, 0.2 }
	plane { < 0, cos(beta), -sin(beta) >, 0 }
	plane { axis(0), 0 }
	pigment {
		color aequatorwinkel
	}
	finish {
		metallic
		specular 0.99
	}
}

#declare linewidth = 0.01;

#macro aequator(phi)
	< cos(phi), 0, sin(phi) >
#end

union {
	#declare phimin = 0;
	#declare phimax = 2 * pi;
	#declare phisteps = 200;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare phi = phimin;
	#declare P = aequator(phi);
	#while (phi < phimax - phistep/2)
		sphere { P, linewidth }
		#declare Pold = P;
		#declare phi = phi + phistep;
		#declare P = aequator(phi);
		cylinder { Pold, P, linewidth }
		sphere { P, linewidth }
	#end
	pigment {
		color aequatorfarbe
	}
	finish {
		metallic
		specular 0.99
	}
}

#macro meridian(theta)
	< cos(longitude) * cos(theta), sin(theta), sin(longitude) * cos(theta) >
#end

union {
	#declare thetamin = 0;
	#declare thetamax = pi/2;
	#declare thetasteps = 100;
	#declare thetastep = (thetamax - thetamin) / thetasteps;
	#declare theta = thetamin;
	#declare P = meridian(theta);
	sphere { P, linewidth }
	#while (theta < thetamax - thetastep/2)
		#declare Pold = P;
		#declare theta = theta + thetastep;
		#declare P = meridian(theta);
		cylinder { Pold, P, linewidth }
		sphere { P, linewidth }
	#end
	
	pigment {
		color meridianfarbe
	}
	finish {
		metallic
		specular 0.99
	}
}

#macro grosskreis(T)
	< cos(T), sin(T) * sin(beta), sin(T) * cos(beta) >
#end

union {
	#declare Tmin = 0;
	#declare Tmax = 2 * pi;
	#declare Tsteps = 200;
	#declare Tstep = (Tmax - Tmin) / Tsteps;
	#declare T = Tmin;
	#declare P = grosskreis(T);
	sphere { P, linewidth }
	#while (T < Tmax - Tstep/2)
		#declare Pold = P;
		#declare T = T + Tstep;
		#declare P = grosskreis(T);
		cylinder { Pold, P, linewidth }
		sphere { P, linewidth }
	#end
	pigment {
		color grosskreisfarbe
	}
	finish {
		metallic
		specular 0.99
	}
}
