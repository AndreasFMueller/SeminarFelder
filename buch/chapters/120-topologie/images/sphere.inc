//
// sphere.inc -- distorted sphere
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "../../../common/common.inc"

place_camera(<-33, 20, 50>, <0, 0, 0>, 16/9, 0.033)
lightsource(<10, 5, 40>, 1, White)

#declare kartoffelfarbe = rgb<0.8,0.8,0.8>;
#declare topfarbe = rgb<0.6,0.8,1.0>;
#declare bottomfarbe = topfarbe;
#declare pfadfarbe = rgb<1.0,0.6,0.8>;

#declare pfadradius = 0.01;
#declare gitterradius = 0.003;

