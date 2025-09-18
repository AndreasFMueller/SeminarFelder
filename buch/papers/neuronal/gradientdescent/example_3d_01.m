% Example 1: Many Maximas and Minimas in 3D

% Define the function f(x, y) = sin(x) * cos(y)
f = @(x, y) sin(x) .* cos(y);

% Create a grid for x and y
x = linspace(-2*pi, 2*pi, 100);
y = linspace(-2*pi, 2*pi, 100);
[X, Y] = meshgrid(x, y);
Z = f(X, Y);

% Plot the 3D surface
figure;
surf(X, Y, Z, 'EdgeColor', 'none');
hold on;
xlabel('x');
ylabel('y');
zlabel('f(x, y)');
title('Function with Multiple Maximas and Minimas in 3D');
colorbar;
grid on;
view(3);

% Initial points for gradient descent
initial_points = [ -2*pi, -2*pi;
                   -2*pi, 0;
                   -2*pi, 2*pi;
                   0, -2*pi;
                   0, 0;
                   0, 2*pi;
                   2*pi, -2*pi;
                   2*pi, 0;
                   2*pi, 2*pi ];

colors = ['r', 'g', 'm', 'c', 'y', 'b', 'k', 'w', 'r'];

% Perform gradient descent for each initial point
for i = 1:size(initial_points, 1)
    x0 = initial_points(i, 1);
    y0 = initial_points(i, 2);
    x_current = x0;
    y_current = y0;
    learning_rate = 0.1;
    max_iterations = 100;
    trajectory_x = x_current;
    trajectory_y = y_current;
    trajectory_z = f(x_current, y_current);
    
    for iter = 1:max_iterations
        grad_x = cos(x_current) * cos(y_current);
        grad_y = -sin(x_current) * sin(y_current);
        x_next = x_current - learning_rate * grad_x;
        y_next = y_current - learning_rate * grad_y;
        trajectory_x(end+1) = x_next;
        trajectory_y(end+1) = y_next;
        trajectory_z(end+1) = f(x_next, y_next);
        if (abs(x_next - x_current) < 1e-6) && (abs(y_next - y_current) < 1e-6)
            break;
        end
        x_current = x_next;
        y_current = y_next;
    end
    
    % Plot the trajectory
    plot3(trajectory_x, trajectory_y, trajectory_z, 'o-', 'Color', colors(i), 'LineWidth', 1.5, 'MarkerSize', 5);
end

hold off;
pause;
