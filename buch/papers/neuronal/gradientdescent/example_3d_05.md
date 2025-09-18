% Definieren der Funktion f(x, y) = x^2 + y^2
f = @(x, y) x.^2 + y.^2;

% Definieren der partiellen Ableitungen
f_x = @(x, y) 2*x;
f_y = @(x, y) 2*y;

% Bereich der x- und y-Werte
x = linspace(-5, 5, 100);
y = linspace(-5, 5, 100);
[X, Y] = meshgrid(x, y);
Z = f(X, Y);

% Erstellen eines transparenten 3D-Drahtgitterdiagramms
figure;
mesh(X, Y, Z, 'EdgeColor', 'b', 'FaceAlpha', 0.3); % Blaues Drahtgitter mit Transparenz
hold on;

% Gradientenabstieg Parameter
learning_rate = 0.1;
num_iterations = 50;
x0 = -4; % Startpunkt x (weiter links)
y0 = 4;  % Startpunkt y (weiter oben)

% Arrays zum Speichern der Werte
x_history = zeros(1, num_iterations + 1);
y_history = zeros(1, num_iterations + 1);
z_history = zeros(1, num_iterations + 1);
x_history(1) = x0;
y_history(1) = y0;
z_history(1) = f(x0, y0);

% Gradientenabstieg
for i = 1:num_iterations
    current_x = x_history(i);
    current_y = y_history(i);
    current_z = z_history(i);
    
    % Berechnen des Gradienten
    grad_x = f_x(current_x, current_y);
    grad_y = f_y(current_x, current_y);
    
    % Aktualisieren der Parameter
    x_history(i + 1) = current_x - learning_rate * grad_x;
    y_history(i + 1) = current_y - learning_rate * grad_y;
    z_history(i + 1) = f(x_history(i + 1), y_history(i + 1));
end

% Zeichnen des Gradientenpfads
plot3(x_history, y_history, z_history, 'r-', 'LineWidth', 2); % Roter Pfad
plot3(x_history(1), y_history(1), z_history(1), 'go', 'MarkerSize', 8, 'MarkerFaceColor', 'g'); % Startpunkt als grüner Kreis
plot3(x_history(end), y_history(end), z_history(end), 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r'); % Endpunkt als roter Kreis

xlabel('x');
ylabel('y');
zlabel('f(x, y)');
title('Transparentes 3D-Drahtgitter mit Gradientenabstiegspfad für f(x, y) = x^2 + y^2');
legend('Drahtgitter', 'Gradientenpfad', 'Startpunkt', 'Endpunkt', 'Location', 'northeast');
grid on;
hold off;
pause;
