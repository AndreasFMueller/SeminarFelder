//
// common.inc
//
// (c) 2025 Prof Dr Andreas Müller
//
#declare M = vnormalize(<1, 1, 1>);
#declare A = vnormalize(<T, 0, 0> + (1-T) * M);
#declare B = vnormalize(<0, 0, T> + (1-T) * M);
#declare C = vnormalize(<0, T, 0> + (1-T) * M);
#declare d = vdot(A, B);
#declare alph = acos(d/(1+d));
#declare R =  pi / (2 * acos(d));
#declare randfarbe = rgb<0.8,0,0.4>;
#declare dreieckfarbe = rgb<1.0,0.8,1.0>;
#declare pfeilfarbe = rgb<0.2,0.6,1.0>;
#declare winkelfarbe = rgb<0.2,0.4,0.2>;

#declare kurvenradius = 0.01;

arrow(O, A, kurvenradius, White)
arrow(O, B, kurvenradius, White)
arrow(O, C, kurvenradius, White)

#macro randkurve(v1, v2)
union {
	#declare n = vnormalize(vcross(v1, v2));
	#declare n2 = vnormalize(-vcross(v1,n));
	#declare phimin = 0;
	#declare phimax = acos(vdot(v1, v2) / (vlength(v1) * vlength(v2)));
	#declare phisteps = 100;
	#declare phistep = (phimax - phimin) / phisteps;
	#declare phi = phimin;
	#declare p = R * (v1 * cos(phi) + n2 * sin(phi));
	sphere { p, kurvenradius }
	#while (phi < phimax - phistep/2)
		#declare pold = p;
		#declare phi = phi + phistep;
		#declare p = R * (v1 * cos(phi) + n2 * sin(phi));
		sphere { p, kurvenradius }
		cylinder { pold, p, kurvenradius }
	#end
	pigment {
		color randfarbe
	}
	finish {
		metallic
		specular 0.99
	}
}
#end

randkurve(A, B)
randkurve(B, C)
randkurve(C, A)

sphere { O, R * 1 - 0.001
	pigment {
		color Gray
	}
	finish {
		metallic
	}
}

intersection {
	sphere { O, R }
	plane { vcross(A, B), 0 }
	plane { vcross(B, C), 0 }
	plane { vcross(C, A), 0 }
	pigment {
		color dreieckfarbe
	}
	finish {
		metallic
		specular 0.5
	}
}

place_camera(R * M + <33, 20, 50>, R * M + zoffset, 16/9, 0.03)
lightsource(R * M + <20, 50, 40>, 1, White)

#declare pl = 0.17 * acos(d) * R;

#declare s = 0;
#declare sstep = 0.2;
#while (s < 0.9)
	#declare phi0 = acos(vdot(A, B));
	#declare n = vnormalize(vcross(A, B));
	#declare n2 = vnormalize(-vcross(A, n));
	#declare phi = phi0 * s;
	#declare p = R * (A * cos(phi) + n2 * sin(phi));
	#declare tangente = -A * sin(phi) + n2 * cos(phi);
	arrow(p, p + pl * tangente, 0.015, pfeilfarbe)
	#declare s = s + sstep;
#end

#declare s = 0;
#while (s < 0.9)
	#declare phi0 = acos(vdot(B, C));
	#declare n = vnormalize(vcross(B, C));
	#declare n2 = vnormalize(-vcross(B, n));
	#declare phi = phi0 * s;
	#declare p = R * (B * cos(phi) + n2 * sin(phi));
	#declare tangente = -B * sin(phi) + n2 * cos(phi);
	#declare n3 = vnormalize(vcross(tangente, p));
	#declare richtung = cos(alph) * tangente + sin(alph) * n3;
	arrow(p, p - pl * richtung, 0.015, pfeilfarbe)
	#declare s = s + sstep;
#end

#declare s = 0;
#while (s < 1.1)
	#declare phi0 = acos(vdot(C, A));
	#declare n = vnormalize(vcross(C, A));
	#declare n2 = vnormalize(-vcross(C, n));
	#declare phi = phi0 * s;
	#declare p = R * (C * cos(phi) + n2 * sin(phi));
	#declare tangente = -C * sin(phi) + n2 * cos(phi);
	#declare n3 = vnormalize(vcross(tangente, p));
	#declare richtung = cos(2 * alph) * tangente + sin(2 * alph) * n3;
	arrow(p, p + pl * richtung, 0.015, pfeilfarbe)
	#declare s = s + sstep;
#end

#declare n = vnormalize(vcross(A, B));
#declare starttangente = vnormalize(-vcross(A, n));
#declare p = R * A;
#declare n = vnormalize(vcross(C, A));
#declare n2 = vnormalize(-vcross(C, n));
#declare tangente = -C * sin(phi0) + n2 * cos(phi0);
#declare n3 = vnormalize(vcross(tangente, p));
#declare endrichtung = cos(2 * alph) * tangente + sin(2 * alph) * n3;

intersection {
	cylinder { (R + 0.002) * A, (R - 0.002) * A, pl }
	plane { vcross(A, B), 0 }
	plane { -vcross(A, endrichtung), 0 }
	pigment {
		color Orange
	}
	finish {
		metallic
		specular 0.9
	}
}

intersection {
	sphere { O, R + 0.002 }
	union {
		cylinder { O, (R + 0.1) * A, pl }
		cylinder { O, (R + 0.1) * B, pl }
		cylinder { O, (R + 0.1) * C, pl }
	}
	plane { vcross(A, B), 0 }
	plane { vcross(B, C), 0 }
	plane { vcross(C, A), 0 }
	pigment {
		color winkelfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}
