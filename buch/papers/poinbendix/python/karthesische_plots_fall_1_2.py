import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from enable_export import enable_export, set_plot_settings

enable_export()

t_span = [0, 100]
t_eval = np.linspace(*t_span, 1000)

# Fall 1:
def fixed_point_omega_set(t, z):
    x, y = z
    dxdt = -x + y*(1-x**2-y**2)
    dydt = -y - x*(1-x**2-y**2)
    return [dxdt, dydt]


initial_conditions = [[0, 0], [1, -1], [1, 2], [-0.25, 2], [-0.75, 1], [-1, -1]]
fig, ax = plt.subplots()
for z0 in initial_conditions:
    sol = solve_ivp(fixed_point_omega_set, t_span, z0, t_eval=t_eval)
    if np.sum(np.diff(sol.y[0])) == 0:
        ax.plot(sol.y[0], sol.y[1], ".", linewidth=0.5)
    ax.plot(sol.y[0], sol.y[1], linewidth=0.5)

set_plot_settings(fig, ax)
fig.savefig("../images/fixed_point_omega_set.pgf")

# Fall 2:
def fall2(t, z):
    x, y = z
    dxdt = y
    dydt = -x
    return [dxdt, dydt]


initial_conditions = [[0, 0], [1, -1], [1, 2], [-0.25, 2], [-0.75, 1], [-1, -1]]
fig, ax = plt.subplots()
for z0 in initial_conditions:
    sol = solve_ivp(fall2, t_span, z0, t_eval=t_eval)
    if np.sum(np.diff(sol.y[0])) == 0:
        ax.plot(sol.y[0], sol.y[1], ".", linewidth=0.5)
    ax.plot(sol.y[0], sol.y[1], linewidth=0.5)

set_plot_settings(fig, ax, 4, 4)
fig.savefig("../images/fall_2.pgf")
