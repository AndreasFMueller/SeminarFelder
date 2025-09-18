//
// torus.inc
//
// (c) 2025 Prof Dr Andreas Müller
//
#declare r = 0.333;
#declare R = 1;

#declare thetastart = -pi;
#declare thetaend = pi;
#declare thetasteps = 48;

#declare phistart = 0;
#declare phiend = 2 * pi;
#declare phisteps = 96;

#macro toruspunkt(phi, theta)
	((R+r*cos(theta)) * <0,cos(phi),sin(phi)> + r * <sin(theta),0,0> )
#end

#macro mytorus()
mesh {
	#declare thetastep = (thetaend - thetastart) / thetasteps;
	#declare phistep = (phiend - phistart) / phisteps;
	#declare phi = phistart;
	#while (phi < phiend - phistep/2)
		#declare theta = thetastart;
		#while (theta < thetaend - thetastep/2)
			triangle {
				toruspunkt(phi, theta),
				toruspunkt(phi, theta + thetastep),
				toruspunkt(phi + phistep, theta + thetastep)
			}
			triangle {
				toruspunkt(phi, theta),
				toruspunkt(phi + phistep, theta + thetastep),
				toruspunkt(phi + phistep, theta)
			}
			#declare theta = theta + thetastep;
		#end
		#declare phi = phi + phistep;
	#end
}
#end

#macro torussection(from, to)
object {
	difference {
		intersection {
			torus { R, r
				rotate <0, 0, 90>
			}
			box { <-2,from,-2>, <2, to, 2> }
		}
		torus { R, 0.99 * r
			rotate <0, 0, 90>
		}
	}
	pigment {
		color rgb<0.8,0.8,0.8>
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#macro kritisch(phi, theta)
sphere {
	toruspunkt(phi, theta), 0.04
	pigment {
		color rgb<1.0,0.8,0.0>
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#declare kurvenradius = 0.02;

#macro aequatorkurve(Phi, Theta, farbe, deltaphi)
union {
	#declare phistep = 2 * deltaphi / phisteps;
	#declare phi = Phi - deltaphi;
	#declare p = toruspunkt(phi, Theta);
	sphere { p, kurvenradius }
	#while (phi < (Phi + deltaphi - phistep/2))
		#declare pold = p;
		#declare phi = phi + phistep;
		#declare p = toruspunkt(phi, Theta);
		cylinder { pold, p, kurvenradius }
		sphere { p, kurvenradius }
	#end
	pigment {
		color farbe
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#macro meridiankurve(Phi, Theta, farbe, deltatheta)
union {
	#declare thetastep = 2 * deltatheta / thetasteps;
	#declare theta = Theta - deltatheta;
	#declare p = toruspunkt(Phi, theta);
	sphere { p, kurvenradius }
	#while (theta < (Theta + deltatheta - thetastep/2))
		#declare pold = p;
		#declare theta = theta + thetastep;
		#declare p = toruspunkt(Phi, theta);
		cylinder { pold, p, kurvenradius }
		sphere { p, kurvenradius }
	#end
	pigment {
		color farbe
	}
	finish {
		metallic
		specular 0.9
	}
}
#end

#macro hoehenlinie(hoehe)
intersection {
	box { <-2, c-0.002, -2>, <2, c + 0.002, 2> }
	torus { R, 1.001 * r
		rotate < 0, 0, 90 >
	}
	pigment {
		//color rgb<0,0.6,0>
		color rgb<0.8,0.4,0>
	}
	finish {
		metallic
		specular 0.9
	}
}
#end
