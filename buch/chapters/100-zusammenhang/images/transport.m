%
% transport.m
%
% (c) 2025 Prof Dr Andreas Müller
%
N = 1801;
dN = (N - 1) / 20;
global r;
r = 0.6;
dt = 2 * pi / N;

function retval = parabola(x, y, x0, y0)
	retval = (x - x0) * (x - x0) + (y - y0) * (y - y0);
end

function retval = hills(x, y)
	retval = 1 - 0.4 * parabola(x, y, 1, 0) * ...
		parabola(x, y, -0.5, sqrt(3)/2) * ...
		parabola(x, y, -0.5, -sqrt(3)/2);
end

function retval = f(x, y)
	retval = exp(-(x^2 + y^2)/2) * hills(x, y);
end

function retval = normalize(v)
	retval = v / norm(v);
end

function retval = metrik(x, y)
	delta = 0.000001;
	tx = [ 1; 0; (f(x + delta, y) - f(x, y)) / delta ];
	ty = [ 0; 1; (f(x, y + delta) - f(x, y)) / delta ];
	g = zeros(2, 2);
	g(1,1) = tx' * tx;
	g(1,2) = tx' * ty;
	g(2,1) = g(1,2);
	g(2,2) = ty' * ty;
	retval = g;
end

function retval = Christoffel1(x, y)
	delta = 0.000001;
	dg = zeros(2, 2, 2);
	dg(:,:,1) = (metrik(x + delta, y) - metrik(x, y)) / delta;
	dg(:,:,2) = (metrik(x, y + delta) - metrik(x, y)) / delta;
	Gamma = zeros(2, 2, 2);
	for i = (1:2)
	for j = (1:2)
	for k = (1:2)
		Gamma(i, j, k) = 0.5 * (dg(j, k, i) + dg(k, i, j) - dg(i, j, k));
	end
	end
	end
	retval = Gamma;
end

function retval = Christoffel2(x, y)
	g = inverse(metrik(x, y));
	Gamma1 = Christoffel1(x, y);
	Gamma2 = zeros(2, 2, 2);
	for k = (1:2)
		Gamma2(:, :, k) = g * [
			Gamma1(1,k,1), Gamma1(2,k,1);
			Gamma1(1,k,2), Gamma1(2,k,2)
		];
	end
	retval = Gamma2;
end

function p = punkt(t)
	global r;
	p = [ r * cos(t) + 0.1, r * sin(t) + 0.1 ];
end

fn = fopen("transportvektoren.inc", "w");


R = eye(2);
for i = (0:N-1)
	t = dt * i;
	p = punkt(t);
	if (0 == rem(i, dN))
		x = p(1);
		y = p(2);
		fprintf(fn, "// i = %d\n", i);
		fprintf(fn, "#declare p = < %.4f, %.4f, %.4f>;\n", ...
			x, f(x, y), y);
		g = metrik(x, y);
		delta = 0.000001;
		fx = (f(x + delta, y) - f(x, y)) / delta;
		fy = (f(x, y + delta) - f(x, y)) / delta;
		l = sqrt(R(:,1)' * g * R(:,1));
		v = [ R(1,1), fx * R(1,1) + fy * R(2,1), R(2,1) ] / l;
		fprintf(fn, "#declare v1 = < %.4f, %.4f, %.4f>;\n", ...
			v(1), v(2), v(3));
		l = sqrt(R(:,2)' * g * R(:,2));
		v = [ R(1,2), fx * R(1,2) + fy * R(2,2), R(2,2) ] / l;
		fprintf(fn, "#declare v2 = < %.4f, %.4f, %.4f>;\n", ...
			v(1), v(2), v(3));
		fprintf(fn, "vektoren(p, v1, v2)\n");
		if (i == 0)
			fprintf(fn, "#declare startvektor1 = v1;\n");
			fprintf(fn, "#declare startvektor2 = v2;\n");
		else
			fprintf(fn, "#declare endvektor1 = v1;\n");
			fprintf(fn, "#declare endvektor2 = v2;\n");
		end
	end
	Gamma = Christoffel2(p(1), p(2));
	tangente = [ -r * sin(t), r * cos(t) ] * dt;
	dR = Gamma(:,:,1) * tangente(1) + Gamma(:,:,2) * tangente(2);
	R = (eye(2) - dR) * R;
end

R
p = punkt(0);
g = metrik(p(1), p(2));

inverse(R) * g * R

fclose(fn);
