#!/usr/bin/env bash
#
# farbseiten.sh -- Formattierung der Farbseiteninfo für die Druckerei
#
# (c) 2020 Prof Dr Andreas Müller, OST Ostschweizer Fachhochschule
#
awk 'BEGIN {
	result = ""
	counter = 0
	base = 0
} 
/^base=/ {
	split($1, a, "=")
	base = a[2]
printf("new base %d\n", base)
	next
}
/^length=/ {
	split($1, a, "=")
	base = base + a[2]
printf("new base %d\n", base)
	next
}
/^#/ {
	next
}
{
	if (length(result) == 0) {
		result = base + $1
	} else {
		result = sprintf("%s,%d", result, base + $1)
	}
	counter++
}
END {
	printf("%s\n", result)
	printf("Anzahl Farbseiten: %d\n", counter)
}' <<EOF
# Kapitel  1
base=4
2
6
# Kapitel  2
base=10
# Kapitel  3
base=20
2
3
8
11
18
24
25
26
27
29
30
# Kapitel  4
base=52
13
19
20
26
29
34
# Kapitel  5
base=88
2
4
11
14
15
20
21
22
25
29
33
# Kapitel  6
base=122
5
7
10
11
# Kapitel  7
base=136
13
14
# Kapitel  8
base=154
5
6
22
# Kapitel  9
base=184
4
6
# Kapitel 10
base=196
2
3
7
# Kapitel 11
base=212
2
5
15
# Kapitel 12: Krümmung
base=238
2
18
21
31
# Kapitel 13: Topologie
base=274
2
4
6
7
13
15
19
20
21
25
32
33
# Kapitel 14 geoalgebra
base=316
4
5
7
8
13
14
15
length=18
# Kapitel 15 nerven
#base=334
2
3
4
5
6
12
13
14
length=14
# Kapitel 16 poinbendix
#base=348
4
6
7
8
10
length=12
# Kapitel 17 elastomechanik
#base=360
length=20
# Kapitel 18 maxwell
#base=380
length=26
# Kapitel 19 diffortho
#base=406
2
5
length=8
# Kapitel 20 helmholtz
#base=414
11
12
length=14
# Kapitel 21 schall
#base=428
length=4
# Kapitel 22 reaktdiff
#base=432
5
10
11
12
14
15
length=16
# Kapitel 23 mongeampere
#base=448
4
5
length=8
# Kapitel 24 mongekant
#base=456
2
6
10
12
14
length=16
# Kapitel 25 neuronal
#base=472
3
6
9
10
11
12
13
14
15
length=16
# Kapitel 26 parallelisierung
#base=488
8
9
10
11
13
14
18
19
20
21
23
length=24
# Kapitel 27 openfoam
#base=512
10
11
13
15
18
length=20
# Kapitel 28 reynolds
#base=532
7
9
length=10
# Kapitel 29 ueberschall
#base=542
5
6
7
9
11
13
14
length=16
# Kapitel 30 wirbelringe
#base=558
2
4
5
8
12
16
length=18
# Kapitel 31 geostrophisch
#base=576
4
5
8
9
12
13
14
15
length=16
# Kapitel 32 rossby
#base=592
3
4
5
7
8
9
12
13
14
length=14
# Kapitel 33 fourier
#base=606
3
6
7
8
9
length=22
# Kapitel 34 particles
#base=628
EOF
