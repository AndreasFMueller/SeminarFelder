import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from enable_export import enable_export, set_polar_plot_settings

# enable_export()

def run_polar_fall_2(t, z):
    r, phi = z
    drdt = r * (1 - r**2)
    dphidt = -1
    return [drdt, dphidt]


# Time span and initial conditions
t_span = [0, 100]
t_eval = np.linspace(*t_span, 1000)
initial_conditions = [
    [2, -np.pi],
    [2, 0],
    [0.25, np.pi / 4],
    [1.5, 3 * np.pi / 5],
]

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
for z0 in initial_conditions:
    sol = solve_ivp(run_polar_fall_2, t_span, z0, t_eval=t_eval)
    ax.plot(sol.y[1], sol.y[0], linewidth=0.5)

radii = np.linspace(0.2, 1.4, 5)
phis = np.linspace(0, 2*np.pi - np.pi/8, 16)
phi, r = np.meshgrid(phis, radii)

drdt, dphidt = run_polar_fall_2(0, (r, phi))

ax.quiver(phi, r, drdt * np.cos(phi) - dphidt * np.sin(phi), drdt * np.sin(phi) + dphidt * np.cos(phi), scale=40, width=0.003)


set_polar_plot_settings(fig, ax, 4, 4)
fig.savefig("../images/fall_2_polar.pgf")


# Fall 3
def run_polar_fall_3(t, z):
    r, phi = z
    drdt = r * (1 - r**2)
    # dphidt = -1 + r * (2 - r) * np.sin(3 * phi)
    dphidt = -1 + (1 - np.abs(r-1)) * np.sin(3 * phi)
    return [drdt, dphidt]


# Time span and initial conditions
t_span = [0, 100]
t_eval = np.linspace(*t_span, 1000)
# initial_conditions = [[0, 0], [0.2, 0.7], [1, -1], [-2, 0]]
initial_conditions = [
    [2, -np.pi],
    [2, 0],
    [0.25, np.pi / 4],
    [1.5, 3 * np.pi / 5],
]

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
for z0 in initial_conditions:
    sol = solve_ivp(run_polar_fall_3, t_span, z0, t_eval=t_eval)
    ax.plot(sol.y[1], sol.y[0], linewidth=0.5)

poles = [[1, np.deg2rad(30)], [1, np.deg2rad(150)], [1, np.deg2rad(270)]]
for z0 in poles:
    assert np.array_equal(run_polar_fall_3(0, z0), [0,0]) 
    ax.plot(z0[1], z0[0], "x:k", ms=10)

drdt, dphidt = run_polar_fall_3(0, (r, phi))

ax.quiver(phi, r, drdt * np.cos(phi) - dphidt * np.sin(phi), drdt * np.sin(phi) + dphidt * np.cos(phi), scale=40, width=0.003)
set_polar_plot_settings(fig, ax, 4, 4)
fig.savefig("../images/fall_3_polar.pgf")
plt.show()
