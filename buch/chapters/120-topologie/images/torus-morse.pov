//
// torus-morse.pov
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

torussection(-1.5, -1 - deltah)
torussection(-1 + deltah, -deltah)
torussection(deltah, 1 - deltah)
torussection(1 + deltah, 1.5)

kritisch(0,0)
kritisch(0,pi)
kritisch(pi,0)
kritisch(pi,pi)

#declare positivfarbe = rgb<0.8,0.2,0.2>;
#declare negativfarbe = rgb<0.2,0.8,1.0>;


aequatorkurve(0, 0, negativfarbe, acos((1 + deltah)/(R+r)))
meridiankurve(0, 0, negativfarbe, acos(deltah/r))

aequatorkurve(0, pi, negativfarbe, acos(deltah/(R-r)))
meridiankurve(0, pi, positivfarbe, acos(deltah/r))

aequatorkurve(pi, pi, positivfarbe, acos(deltah/(R-r)))
meridiankurve(pi, pi, negativfarbe, acos(deltah/r))

aequatorkurve(pi, 0, positivfarbe, acos(deltah/(R+r)))
meridiankurve(pi, 0, positivfarbe, acos(deltah/r))




