% Example 1: Many Maximas and Minimas

% Define the function f(x) = sin(3x) + 0.1x^2
f = @(x) sin(3*x) + 0.1*x.^2;

% Define the gradient of f(x)
grad_f = @(x) 3*cos(3*x) + 0.2*x;

% Range of x
x = linspace(-4, 4, 1000);
y = f(x);

% Plot the function
figure;
plot(x, y, 'b-', 'LineWidth', 2);
hold on;
xlabel('x');
ylabel('f(x)');
title('Function with Multiple Maximas and Minimas');
grid on;

% Initial points for gradient descent
initial_points = [-4, -2, 0, 2, 4];
colors = ['r', 'g', 'm', 'c', 'k'];

% Perform gradient descent for each initial point
for i = 1:length(initial_points)
    x0 = initial_points(i);
    x_current = x0;
    learning_rate = 0.1;
    max_iterations = 100;
    trajectory = x_current;
    
    for iter = 1:max_iterations
        grad = grad_f(x_current);
        x_next = x_current - learning_rate * grad;
        trajectory(end+1) = x_next;
        if abs(x_next - x_current) < 1e-6
            break;
        end
        x_current = x_next;
    end
    
    % Plot the trajectory
    plot(trajectory, f(trajectory), 'o-', 'Color', colors(i), 'LineWidth', 1.5, 'MarkerSize', 5);
end

hold off;
pause;
