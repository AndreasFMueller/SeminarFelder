%
% tetra.m
%
% (c) 2025 Prof Dr Andreas Müller
%
global a = 1;
global d;
d = 0.2;

rand("seed", 4711);

global e1 = [ 1,           0,         0 ];
global e2 = [ 0.5, sqrt(3)/2,         0 ];
global e3 = [ 0,           0, sqrt(6)/3 ];

function retval = punkt(i, j, k)
	global e1;
	global e2;
	global e3;
	global d;
	global a;
	p = i * e1 + j * e2 + k * e3;
	p = p + 0.5 * (1 - (-1)^k) * (e1 + e2) / 3
	d
	retval = a * (p + d * (rand(1,3) - 0.5 * ones(1,3)));
end

fd = fopen("tetrapoints.inc", "w");

for i = (0:6)
	for j = (0:6)
		for k = (0:4)
			p = punkt(i - 3, j - 3, k - 2);
			fprintf(fd, "#declare A_%d_%d_%d = < %.5f, %.5f, %.5f >;\n", i, j, k, p(1), p(3), p(2));
		end
	end
end

fclose(fd);
