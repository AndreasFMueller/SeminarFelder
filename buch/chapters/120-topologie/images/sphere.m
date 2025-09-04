%
% sphere.m
%
% (c) 2025 Prof Dr Andreas Müller
%
rand("seed", 4712)
global n;
n = 6;
global a;
a = 0.40;
T = arrayfun(@(x) (1/(x ^ 0.8)), (1:n)' * (1:n));
T
global A;
A = a * (rand(n, n) - 0.5 * ones(n, n)) .* T;
A(1,1) = 1
global B;
B = a * (rand(n, n) - 0.5 * ones(n, n)) .* T;
B(1,1) = 1
global points;

%A
%B

global steps;
steps = 9;

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

function retval = derivatives(theta, phi)
	global n;
	global A;
	global B;
	Phi = (1:n) * phi;
	Theta = (1:n) * theta;
	retval = zeros(3, 2);
	% phi derivatives
	st = arrayfun(@(theta) (sin(theta)), Theta);
	sp = -(1:n) .* arrayfun(@(phi) sin(phi), Phi);
	retval(1,2) = sum(sum((st' * sp) .* A));
	cp = (1:n) .* arrayfun(@(phi) cos(phi), Phi);
	retval(2,2) = sum(sum((st' * cp) .* A));
	retval(3,2) = 0;
	% theta derivatives
	ct = (1:n) .* arrayfun(@(theta) (cos(theta)), Theta);
	cp = arrayfun(@(phi) cos(phi), Phi);
	retval(1,1) = sum(sum((ct' * cp) .* A));
	sp = arrayfun(@(phi) (sin(phi)), Phi);
	retval(2,1) = sum(sum((ct' * sp) .* B));
	retval(3,1) = -sin(theta);
	% compute angle between tangent vectors
	%a = retval(:,1);
	%b = retval(:,2);
	%winkel = acosd((a' * b) / (norm(a) * norm(b)));
end

function retval = normal(der)
	n = cross(der(:,2), der(:,1));
	retval = n / norm(n);
end

function retval = dgl(x)
	%theta = x(1)
	%phi = x(2)
	d = derivatives(x(1), x(2));
	n = normal(d);
	d(:,3) = n;
	r = cross(d(:,2), n);
	r = r / (-r(3));
	retval = (d \ r)(1:2,1);
end

function retval = Dgl(phi, theta)
	v = dgl([theta, phi]);
	retval = v(2) / v(1);
end

function points = buildpoints(steps)
	wstep = pi / (2 * steps);
	theta = (1:2*steps-1) * wstep;
	phi = (0: 4*steps) * wstep;

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
end

function retval = P(i, k)
	global points;
	retval = reshape(points(i, k, :), 1, 3);
end

function retval = PP(theta, phi)
	p = zeros(1, 3);
	p(1) = x(theta, phi);
	p(2) = y(theta, phi);
	p(3) = cos(theta);
	retval = p;
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

function sphere(fd, p)
	fprintf(fd, "sphere { ");
	punkt(fd, p);
	fprintf(fd, ", pfadradius }\n");
end

function segment(fd, p1, p2)
	fprintf(fd, "cylinder { ");
	punkt(fd, p1);
	fprintf(fd, ", ");
	punkt(fd, p2);
	fprintf(fd, ", pfadradius }\n");
end

function writegitter(fd, steps)
	fprintf(fd, "#macro kartoffel()\n");
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
end

points = buildpoints(80);

fd = fopen("kartoffel.inc", "w");
writegitter(fd, 80);

%for i = (1:10)
%x = rand(1,2) .* [ pi, 2 * pi ]
%dgl(x);
%Dgl(x(2), x(1))
%end
%
%dgl([pi/4,pi/2])
%Dgl(pi/2 , pi/4)

pathsteps = 10;
phistep = pi / (2*pathsteps);
thetastep = pi / 180;
phiend = zeros(1, 4*pathsteps);

fprintf(fd, "#macro toppfade(pfadradius)\n");
theta = (0:30) * thetastep;
for i = (1:4*pathsteps)
	phi = i * phistep;
	fprintf(fd, "// i = %d, phi = %.4f\n", i, phi);
	sphere(fd, PP(theta(1), phi));
	for k = (1:30)
		p1 = PP(theta(k), phi);
		p2 = PP(theta(k+1), phi);
		segment(fd, p1, p2);
		sphere(fd, p2);
	end
end
fprintf(fd, "#end\n");

fprintf(fd, "#macro pfade(pfadradius)\n");
theta = (30:150) * thetastep;
for i = (1:4*pathsteps)
	phi = i * phistep;
	fprintf(fd, "// i = %d, theta = %.4f, phi = %.4f\n", i, theta(1), phi);
	p = PP(theta(1), phi);
	sphere(fd, p);
	path = lsode(@Dgl, phi, theta);
	for k = (1:120)
		p1 = PP(theta(k), path(k));
		p2 = PP(theta(k+1), path(k+1));
		segment(fd, p1, p2);
		sphere(fd, p2);
	end
	phiend(i) = path(121);
end
fprintf(fd, "#end\n");

fprintf(fd, "#macro bottompfade(pfadradius)\n");
theta = (150:180) * thetastep;
for i = (1:4*pathsteps)
	phi = phiend(i);
	fprintf(fd, "// i = %d, phi = %.4f\n", i, phi);
	sphere(fd, PP(theta(1), phi));
	for k = (1:30)
		p1 = PP(theta(k), phi);
		p2 = PP(theta(k+1), phi);
		segment(fd, p1, p2);
		sphere(fd, p2);
	end
end
fprintf(fd, "#end\n");

fprintf(fd, "#macro gitter(pfadradius)\n");
% breitenkreise
theta = (0:180) * thetastep;
for i = (1:4*pathsteps)
	phi = i * phistep;
	fprintf(fd, "// i = %d, phi = %.4f\n", i, phi);
	sphere(fd, PP(theta(1), phi));
	for k = (1:180)
		p1 = PP(theta(k), phi);
		p2 = PP(theta(k+1), phi);
		segment(fd, p1, p2);
		sphere(fd, p2);
	end
end
% meridiane
thetastep = pi / (2 * steps);
theta = (1:2*steps-2) * thetastep;
phistep = pi / 90;
for k = (1:2*steps-2)
	fprintf(fd, "// k = %d, theta = %.4f\n", k, theta(k));
	for i = (0:179)
		p1 = PP(theta(k),  i    * phistep);
		p2 = PP(theta(k), (i+1) * phistep);
		segment(fd, p1, p2);
		sphere(fd, p2);
	end
end
fprintf(fd, "#end\n");

fclose(fd);
