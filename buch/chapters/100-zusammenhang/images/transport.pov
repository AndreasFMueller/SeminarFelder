//
// 3dimage.pov -- -template for 3d images rendered by Povray
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

place_camera(<20, 40, 50>, <0, 0.24, 0>, 16/9, 0.022)
lightsource(<40, 50, 10>, 1, White)

#declare pfadfarbe = rgb<1.0,0.4,0.4>;
#declare flaechenfarbe = rgb<1.0,0.9,0.8>;
#declare vektor1farbe = rgb<0.2,0.8,0.2>;
#declare vektor2farbe = rgb<0.2,0.6,1.0>;

arrow(-e1, e1, 0.01, White)
arrow(-e2, e2, 0.01, White)
arrow(-e3, 1.1 * e3, 0.01, White)

#declare parabola = function(X, Y, X0, Y0) { (X-X0)*(X-X0)+(Y-Y0)*(Y-Y0) }
#declare f = function(X, Y) { 1 - 0.4 * parabola(X, Y, 1, 0) * parabola(X, Y, -0.5, sqrt(3)/2) * parabola(X, Y, -0.5, -sqrt(3)/2) }

#macro punkt(X, Y)
	<X, f(X,Y) * exp(-(X*X+Y*Y)/2), Y>
#end

mesh {
#declare Xmin = -1.5;
#declare Xmax = 1.5;
#declare Xsteps = 400;
#declare Ymin = -1.5;
#declare Ymax = 1.5;
#declare Ysteps = 400;
#declare Xstep = (Xmax - Xmin) / Xsteps;
#declare Ystep = (Ymax - Ymin) / Ysteps;
#declare X = Xmin;
#while (X < Xmax - Xstep/2)
	#declare Y = Ymin;
	#while (Y < Ymax - Ystep/2)
		triangle {
			punkt(X,         Y),
			punkt(X + Xstep, Y),
			punkt(X + Xstep, Y + Ystep)
		}
		triangle {
			punkt(X,         Y),
			punkt(X + Xstep, Y + Ystep),
			punkt(X        , Y + Ystep)
		}
		#declare Y = Y + Ystep;
	#end
	#declare X = X + Xstep;
#end
	pigment {
		color flaechenfarbe
	}
	finish {
		metallic
		specular 0.4
	}
}

#declare pfadlinie = 0.01;
#declare pfadradius = 0.6;

#macro pfadpunkt(phi)
	punkt(pfadradius * cos(phi) + 0.1, pfadradius * sin(phi) + 0.1)
#end

union {
	#declare phimin = 0;
	#declare phimax = 2 * pi;
	#declare phisteps = 200;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare phi = phimin;
	#while (phi < phimax - phistep/2)
		sphere { pfadpunkt(phi), pfadlinie }
		cylinder {
			pfadpunkt(phi),
			pfadpunkt(phi + phistep),
			pfadlinie
		}
		#declare phi = phi + phistep;
	#end
	pigment {
		color pfadfarbe
	}
	finish {
		metallic
		specular 0.99
	}
}

#macro vektoren(p, v1, v2)
arrow(p, p + 0.2 * v1, 0.011, vektor1farbe)
arrow(p, p + 0.2 * v2, 0.011, vektor2farbe)
#end

#include "transportvektoren.inc"

#declare winkelr = 0.15;
#macro winkel(p, r1, r2)
intersection {
	#declare n = vnormalize(vcross(r1, r2));
	cylinder { p - 0.001 * n, p + 0.001 * n, winkelr }
	#declare n1 = -vcross(n, r1);
	plane { n1, vdot(n1, p) }
	#declare n2 = vcross(n, r2);
	plane { n2, vdot(n2, p) }
	pigment {
		color Orange
	}
	finish {
		metallic
		specular 0.99
	}
}
#end

winkel(p, startvektor1, endvektor1)
winkel(p, startvektor2, endvektor2)

