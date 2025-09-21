%
% u.m
%
% (c) 2025 Prof Dr Andreas Müller
%
rand("seed", 4711)

fd = fopen("u.tex", "w");

function retval = polar(r, phi)
	retval = r * [cosd(phi), sind(phi)];
end

d = 0.7;

a = polar(1.8, -30) + d*(rand(1,2)-0.5*ones(1,2));
b = polar(1.8, 210) + d*(rand(1,2)-0.5*ones(1,2));
c = polar(1.8,  90) + d*(rand(1,2)-0.5*ones(1,2));
s = (a + b + c)/3;

o = -0.5;

fprintf(fd, "\\coordinate (A) at (%.4f,%.4f);\n", a(1), a(2)+o);
fprintf(fd, "\\coordinate (B) at (%.4f,%.4f);\n", b(1), b(2)+o);
fprintf(fd, "\\coordinate (C) at (%.4f,%.4f);\n", c(1), c(2)+o);
fprintf(fd, "\\coordinate (S) at (%.4f,%.4f);\n", s(1), s(2)+o);

fclose(fd);
