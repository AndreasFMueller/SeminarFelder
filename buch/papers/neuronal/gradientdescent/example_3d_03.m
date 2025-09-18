% Clear workspace and figures
clear; close all; clc;

% Define the range for x and y, focusing on the back half
x = linspace(0, 2, 100); % Increased resolution for smoother plot
y = linspace(-2, 2, 100);
[X, Y] = meshgrid(x, y);

% Define the loss function L(θ) as a convex function, e.g., a paraboloid
% L(θ) = (x - x_min)^2 + (y - y_min)^2
x_min = 0;
y_min = 0;
L = (X - x_min).^2 + (Y - y_min).^2;

% Plot the 3D surface with more subtle colors
figure;
surf(X, Y, L, 'EdgeColor', 'none');
hold on;

% Use a more subtle colormap by reducing intensity further
colormap(flipud(cool(256) * 0.6)); % Multiply by 0.6 to reduce intensity more

% Add colorbar for reference
colorbar('FontSize', 40);

% Label the axes
xlabel('θ1','FontSize', 40);
ylabel('θ2','FontSize', 40);
zlabel('L(θ)','FontSize', 40);
% title('Back Half of 3D Convex Loss Function with Path and Highlighted Minima');

% Define the starting point and the path
theta_start = [1.5, 1.5]; % Starting point in (x, y) coordinates
learning_rate = 0.1;
num_iterations = 50;

% Convert starting point to grid indices
[~, idx_x_start] = min(abs(x - theta_start(1)));
[~, idx_y_start] = min(abs(y - theta_start(2)));
theta_start_idx = [idx_x_start, idx_y_start];

% Initialize variables for the path
theta_idx = theta_start_idx;
path_X = x(theta_idx(1));
path_Y = y(theta_idx(2));
path_Z = L(theta_idx(1), theta_idx(2));

for i = 1:num_iterations
    % Current position in (x, y)
    current_x = x(theta_idx(1));
    current_y = y(theta_idx(2));

    % Compute the gradient of L(θ) at the current position
    if theta_idx(1) > 1 && theta_idx(1) < size(L, 1) && theta_idx(2) > 1 && theta_idx(2) < size(L, 2)
        grad_L_x = (L(theta_idx(1)+1, theta_idx(2)) - L(theta_idx(1)-1, theta_idx(2))) / (2*(x(2)-x(1)));
        grad_L_y = (L(theta_idx(1), theta_idx(2)+1) - L(theta_idx(1), theta_idx(2)-1)) / (2*(y(2)-y(1)));
    else
        grad_L_x = 0;
        grad_L_y = 0;
    end
    grad_L = [grad_L_x, grad_L_y];

    % Update θ using Gradient Descent
    theta_idx_new = theta_idx - learning_rate * grad_L;

    % Round the indices to the nearest integer
    theta_idx_new = round(theta_idx_new);

    % Ensure that the new indices are within the grid bounds
    theta_idx_new = max(min(theta_idx_new, [length(x), length(y)]), [1, 1]);

    % Append the new point to the path
    path_X(end+1) = x(theta_idx_new(1));
    path_Y(end+1) = y(theta_idx_new(2));
    path_Z(end+1) = L(theta_idx_new(1), theta_idx_new(2));

    % Update theta_idx for the next iteration
    theta_idx = theta_idx_new;
end

% Plot the path with a more subtle color and line style
% plot3(path_X, path_Y, path_Z, 'k-', 'LineWidth', 1.5, 'Color', [0.3, 0.3, 0.3]); % Gray path

% Mark the starting point
% plot3(path_X(1), path_Y(1), path_Z(1), 'go', 'MarkerSize', 6, 'MarkerFaceColor', 'g'); % Starting point

plot3(0.5, 1, 1, 'go', 'MarkerSize', 8, 'LineWidth', 1, 'MarkerFaceColor', 'g'); 

% Highlight the minima at (4, 0, 0) by overlaying a distinct marker
plot3(0.05, 0, 0.05, 'ro', 'MarkerSize', 8, 'LineWidth', 1, 'MarkerFaceColor', 'r'); % Minima marked with a larger red cross
plot3(0.25, 0, 0.05, 'ro', 'MarkerSize', 8, 'LineWidth', 1, 'MarkerFaceColor', 'r'); % Minima marked with a larger red cross

% Add a legend
% legend('Loss Function', 'Path', 'Start', 'Minima', 'Location', 'northwest');
legend('Loss Function', 'Start', 'Minima', 'Gradientabstieg','Location', 'northwest','FontSize', 40);

% Set the view angle for better visualization
view(3);
grid on;
hold off;

% Pause to keep the plot open
pause;

