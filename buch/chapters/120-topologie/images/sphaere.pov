//
// sphaere.pov
//
// (c) 2025 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

place_camera(<33, 7, 10>, <0, 0, 0>, 16/9, 0.0575)
lightsource(<40, 25, -10>, 1, White)


#macro kugelpunkt(phi, theta)
	< sin(theta) * cos(phi), cos(theta), sin(theta) * sin(phi) >
#end

#declare phisteps = 24;
#declare phistart = 0;
#declare phiend = 2 * pi;
#declare phistep = (phiend - phistart) / phisteps;

#declare thetasteps = 12;
#declare thetastart = 0;
#declare thetaend = pi;
#declare thetastep = (thetaend - thetastart) / thetasteps;

#declare r = 0.02;

union {
	sphere { kugelpunkt(0, 0), r/3 }
	#declare phi = phistart;
	#while (phi < phiend - phistep/2)
		cylinder {
			kugelpunkt(phi, thetastart),
			kugelpunkt(phi, thetastart + thetastep),
			r/3
		}
		#declare theta = thetastep;
		#while (theta < thetaend - (3/2) * thetastep)
			sphere { kugelpunkt(phi, theta), r/3 }
			cylinder {
				kugelpunkt(phi, theta),
				kugelpunkt(phi, theta + thetastep),
				r / 3
			}
			cylinder {
				kugelpunkt(phi, theta),
				kugelpunkt(phi + phistep, theta),
				r / 3
			}
			cylinder {
				kugelpunkt(phi, theta),
				kugelpunkt(phi + phistep, theta + thetastep),
				r / 3
			}
			#declare theta = theta + thetastep;
		#end
		sphere { kugelpunkt(phi, theta), r/3 }
		cylinder {
			kugelpunkt(phi, thetaend - thetastep),
			kugelpunkt(phi + phistep, thetaend - thetastep),
			r / 3
		}
		cylinder {
			kugelpunkt(phi, thetaend - thetastep),
			kugelpunkt(phi, thetaend),
			r/3
		}
		#declare phi = phi + phistep;
	#end
	sphere { kugelpunkt(0, thetaend), r/3 }
	pigment {
		color rgb<0.8,0.6,0.4>
	}
	finish {
		specular 0.9
		metallic
	}
}

mesh {
	#declare phi = phistart;
	#while (phi < phiend - phistep/2)
		triangle {
			kugelpunkt(phi, thetastart),
			kugelpunkt(phi, thetastart + thetastep),
			kugelpunkt(phi + phistep, thetastart + thetastep)
		}
		#declare theta = thetastep;
		#while (theta < thetaend - (3/2) * thetastep)
			triangle {
				kugelpunkt(phi, theta),
				kugelpunkt(phi + phistep, theta + thetastep),
				kugelpunkt(phi + phistep, theta)
			}
			triangle {
				kugelpunkt(phi, theta),
				kugelpunkt(phi, theta + thetastep),
				kugelpunkt(phi + phistep, theta + thetastep)
			}
			#declare theta = theta + thetastep;
		#end
		triangle {
			kugelpunkt(phi, theta),
			kugelpunkt(phi, thetaend),
			kugelpunkt(phi + phistep, theta)
		}
		#declare phi = phi + phistep;
	#end
	pigment {
		color rgbt<0.8,0.8,0.8,0.3>
	}
	finish {
		specular 0.9
		metallic
	}
}
