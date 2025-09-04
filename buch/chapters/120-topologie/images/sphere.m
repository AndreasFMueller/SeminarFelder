%
% sphere.m
%
% (c) 2025 Prof Dr Andreas Müller
%
rand("seed", 4711)
global n;
n = 6;
global a;
a = 0.2;
T = arrayfun(@(x) (1/(x ^ 0.8)), (1:n)' * (1:n));
T
global A;
A = a * (rand(n, n) - 0.5 * ones(n, n)) .* T;
A(1,1) = 1
global B;
B = a * (rand(n, n) - 0.5 * ones(n, n)) .* T;
B(1,1) = 1

%A
%B

steps = 40;

function retval = x(theta, phi)
	global n;
	global A;
	Phi = (1:n) * phi;
	Theta = (1:n) * theta;
	st = arrayfun(@(theta) (sin(theta)), Theta);
	cp = arrayfun(@(phi) cos(phi), Phi);
	retval = sum(sum((st' * cp) .* A));
end

function retval = y(theta, phi)
	global n;
	global B;
	Phi = (1:n) * phi;
	Theta = (1:n) * theta;
	st = arrayfun(@(theta) (sin(theta)), Theta);
	sp = arrayfun(@(phi) (sin(phi)), Phi);
	retval = sum(sum((st' * sp) .* B));
end


wstep = pi / (2 * steps);
theta = (1:2*steps-1) * wstep;
phi = (0: 4*steps) * wstep;

global points;
points = zeros(2*steps-1, 4*steps+1, 3);

for (i = (1:2*steps-1))
	z = cos(theta(i));
	for (k = (1:4*steps+1))
%		printf("%d, %d: theta = %.4f, phi = %.4f\n",
%			i, k, theta(i), phi(k));
		points(i, k, 1) = x(theta(i), phi(k));
		points(i, k, 2) = y(theta(i), phi(k));
		points(i, k, 3) = z;
%		printf("%d, %d: %.4f,%4f\n",
%			i, k, points(i, k, 1), points(i, k, 2));
	end
end

%points

function retval = P(i, k)
	global points;
	retval = reshape(points(i, k, :), 1, 3);
end

function punkt(fd, v)
	fprintf(fd, "< %.4f, %.4f, %.4f >", v(1), v(3), v(2));
end

function triangle(fd, p1, p2, p3)
	fprintf(fd, "triangle { ");
	punkt(fd, p1);
	fprintf(fd, ", ");
	punkt(fd, p2);
	fprintf(fd, ", ");
	punkt(fd, p3);
	fprintf(fd, " }\n");
end

function quad(fd, p11, p12, p21, p22)
	triangle(fd, p11, p12, p22)
	triangle(fd, p11, p22, p21)
end

fd = fopen("sphere.inc", "w");
fprintf(fd, "#macro gitter()\n");
fprintf(fd, "// top cap\n");

i = 1;
top = [0, 0, 1];
for k = (1:4*steps)
	p1 = P(i, k);
	p2 = P(i, k+1);
	triangle(fd, p1, p2, top);
end

for i = (1:2*steps-2)
	fprintf(fd, "// ring i = %d\n", i - 1);
	for k = (1:4*steps)
		p11 = P(i, k);
		p21 = P(i, k + 1);
		p12 = P(i + 1, k);
		p22 = P(i + 1, k + 1);
		quad(fd, p11, p12, p21, p22);
	end
end

fprintf(fd, "// bottom cap\n");
i = 2 * steps - 1;
bottom = [0, 0, -1];
for k = (1:4*steps)
	p1 = P(i, k);
	p2 = P(i, k+1);
	triangle(fd, p1, p2, bottom);
end

fprintf(fd, "#end\n");

fclose(fd);
