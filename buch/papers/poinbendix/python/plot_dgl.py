import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from enable_export import enable_export, set_plot_settings

enable_export()



alpha = 1 / 8
epsilon = 0.1
b = 2
gamma = 3 / 4
r = 1 / 4


class RechargeOscillator():
    def __init__(self, alpha, epsilon, b, gamma,  r):
        self.alpha = alpha
        self.epsilon = epsilon
        self.b = b
        self.gamma = gamma
        self.r = r
    def run(self, t, z):
        x, y = z
        dxdt = -x + self.gamma*(self.b*x + y) - self.epsilon*(self.b*x + y)**3
        dydt = -self.r*y - self.alpha* self.b * x
        return [dxdt, dydt]

# Time span and initial conditions
ro = RechargeOscillator(alpha, epsilon, b, gamma, r)
t_span = [0, 100]
t_eval = np.linspace(*t_span, 1000)
# initial_conditions = [[0, 0], [0.2, 0.7], [1, -1], [-2, 0]]
initial_conditions = [[0, 0], [1, -1], [1, 2], [-0.25, 2], [-0.75, 1], [-1, -1]]

# Plotting
fig, ax = plt.subplots()
for z0 in initial_conditions:
    sol = solve_ivp(ro.run, t_span, z0, t_eval=t_eval)
    if np.sum(np.diff(sol.y[0])) == 0:
        ax.plot(sol.y[0], sol.y[1], ".", linewidth=0.5)
    ax.plot(sol.y[0], sol.y[1], linewidth=0.5)

set_plot_settings(fig, ax)
fig.savefig("../images/recharge_oscillator.pgf")

fig, ax = plt.subplots()
for z0 in initial_conditions:
    sol = solve_ivp(ro.run, t_span, z0, t_eval=t_eval)
    ax.plot(sol.y[0], sol.y[1], linewidth=0.5)

set_plot_settings(fig, ax)
fig.savefig("../images/recharge_oscillator_fall_2.pgf")

# Experiment 2: wiggle on parameter alpha
z0 = [1, -1]
alphas = [alpha, alpha + 0.01, alpha - 0.01]
fig, ax = plt.subplots()
for alph in alphas:
    ro = RechargeOscillator(alph, epsilon, b, gamma, r)
    sol = solve_ivp(ro.run, t_span, z0, t_eval=t_eval)
    ax.plot(sol.y[0], sol.y[1], label=f"$\\alpha={alph:.3f}$", linewidth=0.5)
plt.legend()
set_plot_settings(fig, ax)
fig.savefig("../images/recharge_oscillator_alpha.pgf")

# Experiment 3: wiggle on parameter gamma
z0 = [1, -1]
gammas = [gamma, gamma + 0.02, gamma - 0.02]
fig, ax = plt.subplots()
for gamm in gammas:
    ro = RechargeOscillator(alpha, epsilon, b, gamm, r)
    sol = solve_ivp(ro.run, t_span, z0, t_eval=t_eval)
    ax.plot(sol.y[0], sol.y[1], label=f"$\\gamma={gamm:.3f}$", linewidth=0.5)
plt.legend()
set_plot_settings(fig, ax)
fig.savefig("../images/recharge_oscillator_gamma.pgf")

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
