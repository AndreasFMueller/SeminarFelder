% Example 2: Utilizing Gradient Descent to Reach a Minimum

% Define the function f(x) = (x - 2)^2 + 1
f = @(x) (x - 2).^2 + 1;

% Define the gradient of f(x)
grad_f = @(x) 2*(x - 2);

% Range of x
x = linspace(0, 4, 1000);
y = f(x);

% Plot the function
figure;
plot(x, y, 'b-', 'LineWidth', 2);
hold on;
xlabel('x');
ylabel('f(x)');
title('Gradient Descent to Reach a Minimum');
grid on;

% Initial point for gradient descent
x0 = 0;
x_current = x0;
learning_rate = 0.1;
max_iterations = 20;
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
plot(trajectory, f(trajectory), 'ro-', 'LineWidth', 1.5, 'MarkerSize', 5);
hold off;
pause;

