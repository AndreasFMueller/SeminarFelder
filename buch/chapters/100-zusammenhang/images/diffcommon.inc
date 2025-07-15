//
// diffcommon.inc
//
// (c) 2025 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"


arrow(-e1, e1, 0.01, White)
arrow(-e2, e2, 0.01, White)
arrow(-e3, e3, 0.01, White)

#macro kugel(THETA, PHI)
	<  sin(THETA) * cos(PHI),  cos(THETA),  sin(THETA) * sin(PHI) >
#end

#macro ftheta(THETA, PHI)
	<  cos(THETA) * cos(PHI), -sin(THETA),  cos(THETA) * sin(PHI) >
#end
#macro fphi(THETA, PHI)
	< -sin(THETA) * sin(PHI),           0,  sin(THETA) * cos(PHI) >
#end

#declare theta = function(T) { 0.30 * pi + 0.4 * (T - 0.5) - 1 * (T - 0.5) * (T - 0.5) }
#declare phi = function(T) { 1.2 * T + 0.5 }

#declare h = 0.00001;

#declare thetadot = function(T) { (theta(T + h) - theta(T)) / h }
#declare phidot = function(T) { (phi(T + h) - phi(T)) / h }

#macro kurve(T)
	kugel(theta(T), phi(T))
#end

place_camera(<33, 20, 50>, kurve(0.5) + <0,0.1,0>, 16/9, 0.009)
lightsource(<30, 50, 10>, 1, White)

#macro richtung(T)
	ftheta(theta(T), phi(T)) * thetadot(T) + fphi(theta(T), phi(T)) * phidot(T)
#end

#macro tangentialvektor(T, farbe)
	arrow(kurve(T), kurve(T) + 0.25 * vnormalize(richtung(T)), 0.01, farbe)
#end

sphere { O, 1
	pigment {
		color rgb<0.8,0.8,0.8>
	}
	finish {
		metallic
		specular 0.6
	}
}

#declare kurveradius = 0.01;
#declare kurvefarbe = rgb<0.6,0.8,1.0>;

union {
	#declare Tmin = 0.1;
	#declare Tmax = 1;
	#declare Tsteps = 100;
	#declare Tstep = (Tmax - Tmin) / Tsteps;
	#declare T = Tmin;
	#declare P = kurve(T);
	sphere { P, 0.9 * kurveradius }
	#while (T < Tmax - Tstep/2)
		#declare Pold = P;
		#declare T = T + Tstep;
		#declare P = kurve(T);
		cylinder { Pold, P, 0.9 * kurveradius }
		sphere { P, 0.9 * kurveradius }
	#end
	pigment {
		color kurvefarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	#declare gridradius = 0.003;
	#declare Phimin = 0;
	#declare Phimax = pi;
	#declare Phisteps = 12;
	#declare Phistep = (Phimax - Phimin) / Phisteps;
	#declare Thetamin = 0;
	#declare Thetamax = pi/2;
	#declare Thetasteps = 100;
	#declare Thetastep = (Thetamax - Thetamin) / Thetasteps;
	#declare Phi = Phimin;
	#while (Phi < Phimax + Phistep/2)
		#declare Theta = Thetamin;
		#declare P = kugel(Theta, Phi);
		sphere { P, gridradius }
		#while (Theta < Thetamax - Thetastep/2)
			#declare Pold = P;
			#declare Theta = Theta + Thetastep;
			#declare P = kugel(Theta, Phi);
			sphere { P, gridradius }
			cylinder { Pold, P, gridradius }
		#end
		#declare Phi = Phi + Phistep;
	#end
	#declare Phisteps = 100;
	#declare Phistep = (Phimax - Phimin) / Phisteps;
	#declare Thetasteps = 6;
	#declare Thetastep = (Thetamax - Thetamin) / Thetasteps;
	#declare Theta = Thetastep;
	#while (Theta < Thetamax + Thetastep/2)
		#declare Phi = Phimin;
		#while (Phi < Phimax - Phistep/2)
		#declare P = kugel(Theta, Phi);
		sphere { P, gridradius }
			#declare Pold = P;
			#declare Phi = Phi + Phistep;
			#declare P = kugel(Theta, Phi);
			sphere { P, gridradius }
			cylinder { Pold, P, gridradius }
		#end
		#declare Theta = Theta + Thetastep;
	#end
	pigment {
		color Yellow
	}
	finish {
		metallic
		specular 0.9
	}
}

#declare pfeilfarbe = rgb<1.0,0.6,0.6>;
#declare pfeiltransparent = rgbf<1.0,0.6,0.6,0.5>;
#declare T1 = 0.35;
#declare T2 = 0.65;

#macro pfeiltransportiert(T) 
#declare P1 = kurve(T);
#declare P2 = kurve(T2);
#declare axis = vnormalize(vcross(P1, P2));
#declare winkel = acos(vdot(P1, P2));
#declare R = 0.25 * vnormalize(richtung(T2));

#declare Rgedreht = cos(winkel) * R + (1-cos(winkel)) * vdot(axis, R) * axis - sin(winkel) * vcross(axis,R);
arrow(kurve(T), kurve(T) + Rgedreht, 0.01, pfeilfarbe)
#end

