% Example 2: Utilizing Gradient Descent to Reach a Minimum in 3D

% Define the function f(x, y) = (x - 1)^2 + (y - 1)^2
f = @(x, y) (x - 1).^2 + (y - 1).^2;

% Create a grid for x and y
x = linspace(-2, 4, 100);
y = linspace(-2, 4, 100);
[X, Y] = meshgrid(x, y);
Z = f(X, Y);

% Plot the 3D surface
figure;
surf(X, Y, Z, 'EdgeColor', 'none');
hold on;
xlabel('x');
ylabel('y');
zlabel('f(x, y)');
title('Gradient Descent to Reach a Minimum in 3D');
colorbar;
grid on;
view(3);

% Initial point for gradient descent
x0 = -1;
y0 = -1;
x_current = x0;
y_current = y0;
learning_rate = 0.1;
max_iterations = 50;
trajectory_x = x_current;
trajectory_y = y_current;
trajectory_z = f(x_current, y_current);

for iter = 1:max_iterations
    grad_x = 2*(x_current - 1);
    grad_y = 2*(y_current - 1);
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
plot3(trajectory_x, trajectory_y, trajectory_z, 'ro-', 'LineWidth', 2, 'MarkerSize', 5);
hold off;
pause;

