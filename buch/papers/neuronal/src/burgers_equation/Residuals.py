import torch
import numpy as np


def gradients(y, x):
    return torch.autograd.grad(y, x, grad_outputs=torch.ones_like(y),
                               create_graph=True, retain_graph=True)[0]

def burgers_equation_residual(model, t, x):
    t.requires_grad_(True)
    x.requires_grad_(True)
    u_val = model(t, x)
    u_t = gradients(u_val, t)
    u_x = gradients(u_val, x)
    u_xx = gradients(u_x, x)
    return torch.mean((u_t + u_val * u_x - (0.01 / np.pi) * u_xx) ** 2)

def initial_boundary_loss(model, u_d, t_d, x_d):
    u_pred = model(t_d, x_d)
    return torch.mean((u_d - u_pred) ** 2)

