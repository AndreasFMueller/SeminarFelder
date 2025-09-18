%
% bipolar.m -- Koordinatenlinien für bipolares Koordinatensystem
%
% (c) 2025 Prof Dr Andreas Müller
%


umin = -(pi/2) * 0.9;
umax = (pi/2) * 0.9;
vmin = -(pi/2) * 0.9;
vmax = (pi/2) * 0.9;

steps = 18;
smallsteps = 300;

fn = fopen("bipolarpaths.tex", "w");

fprintf(fn, "%%\n");
fprintf(fn, "%% bipolarpaths.tex -- created by bipolar.m, do not modify\n");
fprintf(fn, "%%\n");
fprintf(fn, "%% (c) 2025 Prof Dr Andreas Müller \n");
fprintf(fn, "%%\n");

namecounter = 65;
for u = linspace(umin,umax,steps)
	fprintf(fn, "%% u = %f\n", u);
	fprintf(fn, "\\def\\upath%s{\n", char(namecounter++));
	pointcounter = 0;
	for v = linspace(-pi/2,pi/2,smallsteps)
		if (pointcounter > 0)
			fprintf(fn, "\n\t-- ");
		else
			fprintf(fn, "\t");
		end
		z = coth(u + v * i);
		fprintf(fn, "({%.4f*\\dx},{%.4f*\\dy})", real(z), imag(z));
		pointcounter++;
	end
	fprintf(fn, "\n}\n");
end

namecounter = 65;
for v = linspace(vmin,vmax,steps)
	fprintf(fn, "%% v = %f\n", v);
	fprintf(fn, "\\def\\vpath%s{\n", char(namecounter++));
	pointcounter = 0;
	for u = linspace(-pi/2,pi/2,smallsteps)
		if (pointcounter > 0)
			fprintf(fn, "\n\t-- ");
		else
			fprintf(fn, "\t");
		end
		z = coth(u + v * i);
		fprintf(fn, "({%.4f*\\dx},{%.4f*\\dy})", real(z), imag(z));
		pointcounter++;
	end
	fprintf(fn, "\n}\n");
end

delta = 0.0000001;
fprintf(fn, "\\def\\rechtewinkel{\n");
for v = linspace(vmin,vmax,steps)
	for u = linspace(umin,umax,steps)
		fprintf(fn, "%% u = %f, v = %f\n", u, v);
		z = coth(u + v * i);
		z1 = coth(u + delta + v * i);
		w = arg(z1 - z) * 180 / pi;
		fprintf(fn, "\\rechterwinkel{%.4f}{%.4f}{%.4f}\n",
			real(z), imag(z), w);
	end
end
fprintf(fn, "}\n");

fclose(fn);
