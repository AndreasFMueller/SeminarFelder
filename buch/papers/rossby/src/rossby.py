import numpy as np
import plotly.graph_objects as go

def rossby():
    pass


def random_field(theta, phi):
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    t = np.linspace(0, 2 * np.pi, 25)
    fields = []
    for t_i in t:
        fields.append(np.sin(5 * theta_grid - t_i) ** 2 + 0.2 * np.cos(7 * phi_grid + t_i))
    return fields

def vorticity_field(theta, phi, t=None):
    theta_grid, phi_grid_org = np.meshgrid(theta, phi)

    Omega = 1

    values = []
    for t_i in t:
        phi_grid = phi_grid_org + Omega * t_i  # simple rotation in time
        x = np.sin(theta_grid)*np.cos(phi_grid)
        y = np.sin(theta_grid)*np.sin(phi_grid)
        z = np.cos(theta_grid)
        u = -Omega * y     # vx
        v = Omega * x     # vy
        w =  np.zeros_like(z)
        values.append((x, y, z, u, v, w))

    return values

def zonal_jet_field(theta, phi, t=None):
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Latitude-dependent zonal wind (e.g., strongest at equator)
    U0 = 1
    u = U0 * np.sin(theta_grid)**2  # Eastward velocity varies with latitude

    # No meridional or vertical flow
    v = np.zeros_like(u)
    w = np.zeros_like(u)

    # Spherical to Cartesian coords
    x = np.sin(theta_grid) * np.cos(phi_grid)
    y = np.sin(theta_grid) * np.sin(phi_grid)
    z = np.cos(theta_grid)

    return [(x, y, z, u, v, w)]

def rossby_wave_field(theta, phi, t=None):
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    U0 = 1
    m = 3                # zonal wavenumber
    epsilon = 0.1        # amplitude
    c = 0.5              # westward phase speed

    if t is None:
        t = [0]

    values = []
    for t_i in t:
        # Define streamfunction ψ as a traveling wave
        sin_theta = np.sin(theta_grid)
        # sin_theta = np.clip(sin_theta, 1e-3, None)  # avoid divide-by-small
        psi = epsilon * np.sin(m * phi_grid - c * t_i) * np.sin(theta_grid)**2

        # Compute u = -1/r * ∂ψ/∂θ
        dpsi_dtheta = np.gradient(psi, theta, axis=1)
        u = - dpsi_dtheta / sin_theta
        # Compute v = 1/(r sinθ) * ∂ψ/∂φ
        dpsi_dphi = np.gradient(psi, phi, axis=0)
        v = dpsi_dphi / sin_theta
        # Add background zonal jet to u
        u += U0 * np.sin(theta_grid)**2

        # No radial flow
        w = np.zeros_like(u)

        # Sphere surface
        x = np.sin(theta_grid) * np.cos(phi_grid)
        y = np.sin(theta_grid) * np.sin(phi_grid)
        z = np.cos(theta_grid)
        values.append((x, y, z, u, v, w))

    return values