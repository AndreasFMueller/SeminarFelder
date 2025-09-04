//
// kartoffel.pov -- distorted sphere
//
// (c) 2023 Prof Dr Andreas Müller
//
#include "sphere.inc"
#include "kartoffel.inc"

mesh {
	kartoffel()
	pigment {
		color kartoffelfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	pfade(pfadradius)
	pigment {
		color pfadfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	toppfade(pfadradius)
	pigment {
		color topfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	bottompfade(pfadradius)
	pigment {
		color bottomfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}

union {
	gitter(gitterradius)
	pigment {
		color kartoffelfarbe
	}
	finish {
		metallic
		specular 0.9
	}
}
