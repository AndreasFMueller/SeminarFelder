from scipy.stats import qmc
import torch
import numpy as np

lhs = qmc.LatinHypercube(d=1)
lhs_2d = qmc.LatinHypercube(d=2)
N_ic, N_bc1, N_bc2 = 2000, 1000, 1000 #50, 25, 25
N_c = 5000 #10000

def get_data(device):
    # Initial & boundary data
    t_d = lhs.random(n=N_ic)  # 2000 t-Werte
    t_d_test = t_d[:int(0.2 * N_ic)]
    t_d = t_d[int(0.2 * N_ic):]
    zeros = np.zeros((N_ic, 1))
    zeros_test = zeros[:int(0.2 * N_ic)]
    zeros = zeros[int(0.2 * N_ic):]

    t_d = np.append(zeros, t_d, axis=0)  # 2000 mal 0 + vorherige 2000 t-Werte = 4000
    t_d_test = np.append(zeros_test, t_d_test, axis=0)

    x_d = lhs.random(n=N_ic)  # 2000 x-Werte
    x_d = 2 * (x_d - 0.5)  # Intervall von x-Werten auf [-1,1] anpassen
    x_d_test = x_d[:int(0.2 * N_ic)]
    x_d = x_d[int(0.2 * N_ic):]
    neg_ones = -1 * np.ones((N_bc1, 1))
    neg_ones_test = neg_ones[:int(0.2 * N_bc1)]
    neg_ones = neg_ones[int(0.2 * N_bc1):]
    pos_ones = +1 * np.ones((N_bc2, 1))
    pos_ones_test = pos_ones[:int(0.2 * N_bc2)]
    pos_ones = pos_ones[int(0.2 * N_bc2):]

    x_d = np.append(x_d, neg_ones, axis=0)  # vorherige 2000 x-Werte + 1000 mal -1 = 3000
    x_d = np.append(x_d, pos_ones, axis=0)  # vorherige 3000 x-Werte + 1000 mal 1 = 4000
    x_d_test = np.append(x_d_test, neg_ones_test, axis=0)
    x_d_test = np.append(x_d_test, pos_ones_test, axis=0)

    u_d = np.zeros_like(x_d)  # 4000 mal 0
    u_d[:N_ic] = -np.sin(np.pi * x_d[:N_ic])
    # zu den ersten 2000 Werten gehören die ersten 2000 aus x_d und t_d, zu den zweiten 2000 die zweiten 2000 aus x_d und t_d
    # erste 2000: u von Anfangsbedingung, x in [-1,1], t = 0
    # zweite 2000: u = 0, x = -1 oder x = 1, t in [0,1]
    u_d_test = np.zeros_like(x_d_test)
    u_d_test[:int(0.2 * N_ic)] = -np.sin(np.pi * x_d_test[:int(0.2 * N_ic)])

    # Main data for burgers equation residual
    points = lhs_2d.random(n=N_c)
    points[:, 1] = 2 * (points[:, 1] - 0.5)

    t_c = points[:, [0]]  # [0,1) --> 5000 Punkte
    x_c = points[:, [1]]  # [-1,1) --> 5000 Punkte
    t_c_test = t_c[:int(0.2 * N_c)]
    t_c = t_c[int(0.2 * N_c):]
    x_c_test = x_c[:int(0.2 * N_c)]
    x_c = x_c[int(0.2 * N_c):]

    x_d = torch.tensor(x_d, device=device)
    t_d = torch.tensor(t_d, device=device)
    u_d = torch.tensor(u_d, device=device)
    x_c = torch.tensor(x_c, device=device)
    t_c = torch.tensor(t_c, device=device)
    x_d_test = torch.tensor(x_d_test, device=device)
    t_d_test = torch.tensor(t_d_test, device=device)
    u_d_test = torch.tensor(u_d_test, device=device)
    x_c_test = torch.tensor(x_c_test, device=device)
    t_c_test = torch.tensor(t_c_test, device=device)

    train_data = [x_d, t_d, x_c, t_c, u_d]
    test_data = [x_d_test, t_d_test, x_c_test, t_c_test, u_d_test]

    return train_data, test_data