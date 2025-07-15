import numpy as np
import torch
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from Residuals import total_loss

matplotlib.use('TkAgg')

# Plots train & test error over training epochs
def error_plot(train_error, test_error):
    epochs = range(1, len(train_error) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_error, label='Training Error')
    plt.plot(epochs, test_error, label='Test Error')
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.title('Errors over Epochs')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Evaluates the model at random x and y values in the ranges (-1, 1)
# Creates a contour plot at a single timestep t (t is fixed at 0.5)
def plot_solution(model, device, t_fixed=0.5):
    grid_size = 100
    x_vals = np.linspace(-1, 1, grid_size)
    y_vals = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x_vals, y_vals)

    xy_t = torch.FloatTensor(np.column_stack([X.ravel(), Y.ravel(), np.full_like(X.ravel(), t_fixed)])).to(device)
    U_pred = model(xy_t).cpu().detach().numpy().reshape(grid_size, grid_size)

    plt.figure(figsize=(6, 5))
    plt.contourf(X, Y, U_pred, levels=100, cmap='coolwarm')
    plt.colorbar(label='Wave Height')
    plt.title(f"Wave solution at t = {t_fixed}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

# Same as above but updates at every second for t values in [0; 1]
def animate_solution(model, device):
    error = []
    grid_size = 1000
    t_values = np.linspace(0, 10, 51)
    x_vals = np.linspace(-10, 10, grid_size)
    y_vals = np.linspace(-10, 10, grid_size)
    X, Y = np.meshgrid(x_vals, y_vals)

    u_pred_array = []

    for t in t_values:
        xyt = torch.FloatTensor(
            np.column_stack([X.ravel(), Y.ravel(), np.full_like(X.ravel(), t)])
        ).to(device)
        u_pred_array.append(model(xyt).cpu().detach().numpy().reshape(grid_size, grid_size))

        x = torch.FloatTensor(np.column_stack([X.ravel()])).to(device)
        y = torch.FloatTensor(np.column_stack([Y.ravel()])).to(device)
        t = torch.FloatTensor(np.column_stack([np.full_like(X.ravel(), t)])).to(device)
        error.append(total_loss(model, x, y, t, device).item())

    print(f"Average loss on animated data: {np.mean(error)}")

    fig, ax = plt.subplots(figsize=(20, 20))

    cbar = None

    def update(frame):
        nonlocal cbar
        t = t_values[frame]
        U_pred = u_pred_array[frame]

        cont = ax.contourf(X, Y, U_pred, levels=100, cmap='coolwarm')
        ax.set_title(f"Wave solution at t = {t:.1f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        if cbar is None:
            cbar = fig.colorbar(cont, ax=ax, label='Wave Height')

    ani = animation.FuncAnimation(fig, update, frames=len(t_values), interval=100, repeat=True)
    ani.save("wave_animation.gif", writer='pillow', fps=5)
    plt.show()