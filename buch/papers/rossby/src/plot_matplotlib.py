import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import cartopy.io.shapereader as shpreader


def plot_lon_lat_lines(ax, n_latitudes, n_longitudes, theta, phi):
    # Longitude lines (meridians)
    for p in np.linspace(0, 2 * np.pi, n_latitudes):
        x_line = np.sin(theta) * np.cos(p)
        y_line = np.sin(theta) * np.sin(p)
        z_line = np.cos(theta)
        ax.plot(x_line, y_line, z_line, color="black", linewidth=0.5)

    # Latitude lines (parallels)
    for t in np.linspace(-np.pi / 2, np.pi / 2, n_longitudes):
        x_line = np.cos(t) * np.cos(phi)
        y_line = np.cos(t) * np.sin(phi)
        z_line = np.full_like(phi, np.sin(t))
        ax.plot(x_line, y_line, z_line, color="black", linewidth=0.5)


def plot_coastline(ax):
    coastline_data = get_coastline()
    for coords in coastline_data:
        lon, lat = coords
        lon = np.radians(lon)
        lat = np.radians(lat)
        x_coast = np.cos(lat) * np.cos(lon)
        y_coast = np.cos(lat) * np.sin(lon)
        z_coast = np.sin(lat)
        ax.plot(x_coast, y_coast, z_coast, color="black", linewidth=0.5)

def get_coastline():
    reader = shpreader.Reader(
        shpreader.natural_earth(
            resolution="110m", category="physical", name="coastline"
        )
    )
    coastlines = []
    for record in reader.records():
        coords = (
            np.array(record.geometry.coords.xy)
            if record.geometry.geom_type == "LineString"
            else None
        )
        if coords is not None:
            coastlines.append(coords)
    return coastlines


def animate_sphere(theta, phi, fields):
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    x = np.sin(theta_grid) * np.cos(phi_grid)
    y = np.sin(theta_grid) * np.sin(phi_grid)
    z = np.cos(theta_grid)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_axis_off()
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#1e1e1e")

    plot_lon_lat_lines(ax, len(theta), len(phi), theta, phi)
    plot_coastline(ax)

    surf = [
        ax.plot_surface(
            x,
            y,
            z,
            facecolors=plt.cm.viridis(fields[0]),
            rstride=1,
            cstride=1,
            antialiased=False,
        )
    ]

    def update(i):
        surf[0].remove()
        surf[0] = ax.plot_surface(
            x,
            y,
            z,
            facecolors=plt.cm.viridis(fields[i]),
            rstride=1,
            cstride=1,
            antialiased=False,
        )

    # ani = FuncAnimation(fig, update, frames=len(fields), interval=50)
    # ani.save("sphere_animation.mp4", fps=20)
    plt.show()
    plt.close()

def plot_sphere_with_quiver(values):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")

    # Sphere grid
    theta = np.linspace(0, np.pi, 40)
    phi = np.linspace(0, 2 * np.pi, 80)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    x = np.sin(theta_grid) * np.cos(phi_grid)
    y = np.sin(theta_grid) * np.sin(phi_grid)
    z = np.cos(theta_grid)

    # White sphere
    ax.plot_surface(x, y, z, color='white', rstride=1, cstride=1, alpha=1, edgecolor='none')

    # Lines & coast
    plot_lon_lat_lines(ax, 12, 12, theta_grid[:, 0], phi_grid[0])
    plot_coastline(ax)

    # Quiver
    for xq, yq, zq, u, v, w in values:
        ax.quiver(
            xq, yq, zq,
            u, v, w,
            length=0.1, normalize=True, color="blue", linewidth=0.5
        )

    plt.show()