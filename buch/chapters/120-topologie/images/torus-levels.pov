//
// torus-levels.pov
//
// (c) 2025 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

place_camera(<23, 20, 20>, <0, 0.02, 0>, 16/9, 0.07)
lightsource(<40, 35, -10>, 10, White)

#include "torus.inc"

arrow(<-0.5,0,0>, <0.5,0,0>, 0.013, White)
arrow(<0,-1.5,0>, <0,1.5,0>, 0.013, White)
arrow(<0,0,-1.5>, <0,0,1.5>, 0.013, White)

#declare deltah = 0.14;

torussection(-1.5, 1.5)

kritisch(0,0)
kritisch(0,pi)
kritisch(pi,0)
kritisch(pi,pi)

#declare csteps = 48;
#declare cstart = -1.333;
#declare cend = 1.333;
#declare cstep = (cend - cstart) / csteps;
#declare c = cstart;
#while (c < cend + cstep/2)
	hoehenlinie(c)
	#declare c = c + cstep;
#end
