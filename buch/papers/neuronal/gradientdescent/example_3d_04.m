% Definieren der Funktion
f = @(x, y) x.^2 - y.^2;

% Bereich der x- und y-Werte
x = linspace(-5, 5, 100);
y = linspace(-5, 5, 100);
[X, Y] = meshgrid(x, y);
Z = f(X, Y);

% Erstellen eines Konturdiagramms
figure;
contourf(X, Y, Z, 50, 'LineColor', 'none');
colorbar;
xlabel('x');
ylabel('y');
title('Konturdiagramm für f(x, y) = x^2 - y^2');
pause;
