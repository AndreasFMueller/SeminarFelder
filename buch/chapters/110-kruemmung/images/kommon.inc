//
// kommon.inc -- common stuff for kruemmung
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

#declare flaechenfarbe = rgb<0.4,0.6,0.8>;
#declare gitterfarbe = rgb<1.0,0.6,0.8>;
#declare gitterradius = 0.005;
#declare achsradius = 0.008;
#declare strahlenfarbe = rgb<0.8,0.0,0.0>;
#declare verbindungsfarbe = rgb<1.0,0.6,0.2>;

place_camera(<33, 20, 50>, <0, -0.095, 0>, 16/9, 0.018)
lightsource(<40, 50, 10>, 1, White)

//arrow(-1.1 * e1, 1.1 * e1, achsradius, White)
//arrow(-0.5 * e2, 0.5 * e2, achsradius, White)
//arrow(-1.1 * e3, 1.1 * e3, achsradius, White)

#declare f = function(PHI) { -sin(2 * PHI) * (abs(K)-K)/2 + (-1) * (abs(K)+K)/2 }

#declare radiusfunktion = function(R) { (R * R) }

#macro F(PHI, R)
	< R * cos(PHI), 0.3 * f(PHI) * radiusfunktion(R), R * sin(PHI) >
#end

#declare phimin = 0;
#declare phimax = 2 * pi;
#declare rmin = 0;
#declare rmax = 1;

mesh {
	#declare phisteps = 120;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare rsteps = 80;
	#declare rstep = (rmax - rmin) / rsteps;

	#declare phi = phimin;
	#while (phi < phimax - phistep/2)
		// Dreieck für r=0
		triangle {
			F(0, 0),
			F(phi, rstep),
			F(phi + phistep, rstep)
		}
		// quads
		#declare r = rstep;
		#while (r < rmax - rstep/2)
			triangle {
				F(phi, r),
				F(phi + phistep, r),
				F(phi + phistep, r + rstep)
			}
			triangle {
				F(phi, r),
				F(phi + phistep, r + rstep),
				F(phi, r + rstep)
			}
			#declare r = r + rstep;
		#end
		#declare phi = phi + phistep;
	#end
	pigment {
		color flaechenfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#macro strahl(PHI)
	#declare r = rmin;
	#declare P = F(PHI, r);
	#while (r < rmax - rstep/2)
		#declare Pold = P;
		#declare r = r + rstep;
		#declare P = F(PHI, r);
		cylinder { Pold, P, gitterradius }
		sphere { P, gitterradius }
	#end
#end

#macro kreis(R)
	#declare phi = phimin;
	#declare P = F(phi, R);
	#while (phi < phimax - phistep/2)
		#declare Pold = P;
		#declare phi = phi + phistep;
		#declare P = F(phi, R);
		cylinder { Pold, P, gitterradius }
		sphere { P, gitterradius }
	#end
#end

union {
	#declare phisteps = 24;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare rsteps = 40;
	#declare rstep = (rmax - rmin) / rsteps;

	#declare phi = phimin;
	#while (phi < phimax - phistep/2)
		strahl(phi)
		#declare phi = phi + phistep;
	#end

	#declare phisteps = 240;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare rsteps = 10;
	#declare rstep = (rmax - rmin) / rsteps;

	#declare r = rstep;
	#while (r < rmax + rstep/2)
		kreis(r)
		#declare r = r + rstep;
	#end
	pigment {
		color gitterfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare phimin = 5 * pi / 12;
#declare phimax = 7 * pi / 12;

#declare gitterradius = 1.1 * gitterradius;

union {
	#declare rsteps = 10;
	#declare rstep = (rmax - rmin) / rsteps;
	#declare r = rstep;
	#while (r < rmax + rstep/2)
		kreis(r)
		#declare r = r + rstep;
	#end
	pigment {
		color verbindungsfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare gitterradius = 1.4 * gitterradius;

union {
	#declare rsteps = 40;
	#declare rstep = (rmax - rmin) / rsteps;
	strahl(phimin)
	strahl(phimax)
	pigment {
		color strahlenfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}


