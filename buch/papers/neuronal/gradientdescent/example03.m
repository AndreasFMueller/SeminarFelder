% Example 3: Poorly Chosen Gradient Descent Near a Minimum

% Define the function f(x) = x^4 - 4x^2 + 3
f = @(x) x.^4 - 4*x.^2 + 3;

% Define the gradient of f(x)
grad_f = @(x) 4*x.^3 - 8*x;

% Range of x
x = linspace(-2.5, 2.5, 1000);
y = f(x);

% Plot the function
figure;
plot(x, y, 'b-', 'LineWidth', 2);
hold on;
xlabel('x');
ylabel('f(x)');
title('Poorly Chosen Gradient Descent Near a Minimum');
grid on;

% Initial point for gradient descent
x0 = 1.5;
x_current = x0;
learning_rate = 1; % Large learning rate
max_iterations = 10;
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
