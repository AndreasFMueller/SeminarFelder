import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import torch

matplotlib.use('TkAgg')

def error_plot(train_error, test_error):
    plt.figure(figsize=(6, 3))
    plt.semilogy(train_error, label="L(theta)")
    plt.semilogy(test_error, label="L^1(theta)")
    plt.xlabel("Epoch")
    plt.ylabel("Error")
    plt.title("Verlauf Approximationsfehler")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def solution_plot(model, device):
    n, m = 100, 200
    X = np.linspace(-1, +1, m)
    T = np.linspace(0, 1, n)
    X0, T0 = np.meshgrid(X, T)

    X_flat = torch.tensor(X0.reshape(-1, 1), device=device)
    T_flat = torch.tensor(T0.reshape(-1, 1), device=device)

    with torch.no_grad():
        U = model(T_flat, X_flat).cpu().numpy().reshape(n, m)

    plt.figure(figsize=(8, 4), dpi=150)
    plt.pcolormesh(T0, X0, U, cmap='coolwarm', shading='auto')
    plt.colorbar(label="u(x, t)")
    plt.xlim(0, 1)
    plt.ylim(-1, 1)
    plt.xlabel("t")
    plt.ylabel("x")
    plt.title(f"1D Burgers-Gleichung")
    plt.tight_layout()
    plt.show()
