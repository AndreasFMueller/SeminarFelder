import numpy as np
import plotly.graph_objects as go
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import time
import os
import plotly.io as pio
import plotly.figure_factory as ff
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Plot_Sphere:
    def __init__(
        self,
        theta,
        phi,
        fields=None,
        plot_coastlines=True,
        plot_lonlat_lines=True,
        stride_longitudes=1,
        stride_latitudes=1,
    ):
        self.theta = theta
        self.phi = phi
        self.fields = fields
        self.plot_coastlines = plot_coastlines
        self.plot_lonlat_lines = plot_lonlat_lines
        self.n_longitudes = len(phi)
        self.n_latitudes = len(theta)
        self.stride_longitudes = stride_longitudes
        self.stride_latitudes = stride_latitudes

    # Function to get coastline data
    def get_coastline(self):
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

    def plot_lon_lat_lines(self):

        # Longitude lines (meridians)
        longitude_lines = []

        for p in self.phi[:: self.stride_longitudes]:
            x_line = np.sin(self.theta) * np.cos(p)
            y_line = np.sin(self.theta) * np.sin(p)
            z_line = np.cos(self.theta)
            longitude_lines.append(
                go.Scatter3d(
                    x=x_line,
                    y=y_line,
                    z=z_line,
                    mode="lines",
                    line=dict(color="black", width=2),
                )
            )

        # Latitude lines (parallels)
        latitude_lines = []
        for t in np.linspace(
            -np.pi / 2, np.pi / 2, self.n_latitudes // self.stride_latitudes
        ):
            x_line = np.cos(t) * np.cos(self.phi)
            y_line = np.cos(t) * np.sin(self.phi)
            z_line = np.full_like(self.phi, np.sin(t))
            latitude_lines.append(
                go.Scatter3d(
                    x=x_line,
                    y=y_line,
                    z=z_line,
                    mode="lines",
                    line=dict(color="black", width=2),
                    showlegend=False,
                )
            )

        return longitude_lines, latitude_lines

    def plot_coastline(self):
        coastline_data = self.get_coastline()
        coastline = []
        for coords in coastline_data:
            lon, lat = coords
            lon = np.radians(lon)
            lat = np.radians(lat)
            x_coast = np.cos(lat) * np.cos(lon)
            y_coast = np.cos(lat) * np.sin(lon)
            z_coast = np.sin(lat)
            coastline.append(
                go.Scatter3d(
                    x=x_coast,
                    y=y_coast,
                    z=z_coast,
                    mode="lines",
                    line=dict(color="black", width=2),
                )
            )
        return coastline

    def animate_sphere(self, static_traces, changing_traces):
        t = time.time()
        camera = dict(
            eye=dict(
                x=1.25, y=1.25, z=1.25
            )  # or pull this from fig.layout.scene.camera
        )
        frames = [
            go.Frame(
                data=(static_traces + [trace]),
                name=str(i),
                layout=go.Layout(title_text=f"Frame {i}", scene_camera=camera),
            )
            for i, trace in enumerate(changing_traces)
        ]
        print("Time to create frames:", time.time() - t)
        # fig = go.Figure(frames[0])
        fig = go.Figure(
            data=static_traces + [changing_traces[0]],
            layout=go.Layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Play",
                                method="animate",
                                args=[
                                    None,
                                    {
                                        "frame": {"duration": 10, "redraw": True},
                                    },
                                ],
                            )
                        ],
                    )
                ],
            ),
            frames=frames,
        )
        fig.update_layout(height=850, showlegend=False)
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor="rgba(0,0,0,0)",  # transparent background
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_layout(
            scene_camera=dict(projection=dict(type="orthographic"))  # optional
        )

        return fig

    def plot_sphere(self, vaules=None):
        traces = self.plot_sphere_static() + [self.plot_sphere_surface(vaules)]
        return traces

    def animate_sphere_multiple_figs(self):
        figs = []
        for field in self.fields:
            figs.append(
                self.make_fig(
                    [self.plot_sphere_surface(field)] + self.plot_sphere_static()
                )
            )
        return figs

    def plot_sphere_surface(self, values=None):
        if values is None:
            # Create a dummy surface
            theta_grid, phi_grid = np.meshgrid(self.theta, self.phi)
            x = np.sin(theta_grid) * np.cos(phi_grid)
            y = np.sin(theta_grid) * np.sin(phi_grid)
            z = np.cos(theta_grid)
            magnitude = None
            return go.Surface(
                x=x,
                y=y,
                z=z,
                surfacecolor=np.ones_like(z),  # or any constant array
                colorscale=[[0, "white"], [1, "white"]],
                cmin=0,
                cmax=1,
                showscale=False,
                opacity=1,
            )
        else:
            traces = []
            for value in values:
                # Unpack the values
                x = value[0]
                y = value[1]
                z = value[2]
                u = value[3]
                v = value[4]
                w = value[5]
                magnitude = np.sqrt(u**2 + v**2 + w**2)
                trace = go.Surface(
                    x=x,
                    y=y,
                    z=z,
                    surfacecolor=magnitude,
                    colorscale="Viridis",
                    opacity=1,
                    showscale=False,
                )
                traces.append(trace)
            return traces

    def euler_streamline(self, x0, y0, f, steps=50, h=0.1):
        x_vals, y_vals = [x0], [y0]
        for _ in range(steps):
            vx, vy = f(x_vals[-1], y_vals[-1])
            x_vals.append(x_vals[-1] + vx * h)
            y_vals.append(y_vals[-1] + vy * h)
        return x_vals, y_vals

    def streamline(self, values):
        figs = []
        for value in values:
            theta = np.arccos(value[2])
            phi = np.arctan2(value[1], value[0])
            u = value[3]
            v = value[4]

            lat = np.rad2deg(np.pi / 2 - theta)
            lon = np.rad2deg(phi)
            u_clean = np.nan_to_num(u, nan=0.0, posinf=0.0, neginf=0.0)
            v_clean = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
            # Flatten
            x = np.linspace(0, 2 * np.pi, 20)
            y = np.linspace(-np.pi / 2, np.pi / 2, 20)
            fig = ff.create_streamline(x, y, u_clean, v_clean, arrow_scale=0.1)
            figs.append(fig)
        return figs

    def cone_plot3D(self, values):
        traces = []
        for value in values:
            x = value[0]
            y = value[1]
            z = value[2]
            u = value[3]
            v = value[4]
            w = value[5]
            trace = go.Cone(
                x=x.flatten(),
                y=y.flatten(),
                z=z.flatten(),
                u=u.flatten(),
                v=v.flatten(),
                w=w.flatten(),
                colorscale="Viridis",
                sizemode="absolute",
                sizeref=1,
            )
            traces.append(trace)
        return traces

    def rossby_surface_with_flow(self, values):
        traces = []
        for value in values:
            x = value[0]
            y = value[1]
            z = value[2]
            u = value[3]
            v = value[4]
            w = value[5]

            # Cone: velocity vectors (x, y, z: locations; u, v, w: flow)
            traces.append(
                go.Cone(
                    x=x.flatten(),
                    y=y.flatten(),
                    z=z.flatten() + 0.2,
                    u=u.flatten(),
                    v=v.flatten(),
                    w=w.flatten(),
                    colorscale="Viridis",
                    sizemode="absolute",
                    sizeref=1,
                    anchor="tip",
                    showscale=False,
                )
            )

            magnitude = np.sqrt(u**2 + v**2 + w**2)
            # # Surface: assumes x, y, z represent scalar field like ψ or height
            traces.append(
                go.Surface(
                    x=x,
                    y=y,
                    z=z,
                    colorscale="Viridis",
                    opacity=0.6,
                    showscale=False,
                    surfacecolor=magnitude,
                )
            )

        return traces

    def streamtube_plot(self, values):
        traces = []
        for value in values:
            x = value[0]
            y = value[1]
            z = value[2]
            u = value[3]
            v = value[4]
            w = value[5]
            trace = go.Streamtube(
                x=x.flatten(),
                y=y.flatten(),
                z=z.flatten(),
                u=u.flatten(),
                v=v.flatten(),
                w=w.flatten(),
                colorscale="Viridis",
                sizeref=1,
            )
            traces.append(trace)
        return traces

    def plot_sphere_static(self):

        coastline = []
        if self.plot_coastlines:
            coastline = self.plot_coastline()

        longitude_lines = []
        latitude_lines = []
        if self.plot_lonlat_lines:
            longitude_lines, latitude_lines = self.plot_lon_lat_lines()

        traces = longitude_lines + latitude_lines + coastline

        return traces

    def make_fig(self, traces):
        fig = go.Figure(data=traces)

        # Set layout
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            showlegend=False,
            width=1000,
            height=1000,
            uirevision="keep",  # preserves 3D view
        )

        return fig

    def make_rotating_figs(self, traces, n=8):
        figs = []
        for i in range(n):
            angle = -2 * np.pi * i / n
            camera = dict(eye=dict(x=2 * np.cos(angle), y=2 * np.sin(angle), z=0.8))

            fig = go.Figure(data=traces)
            fig.update_layout(
                scene=dict(
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    zaxis=dict(visible=False),
                    camera=camera,
                ),
                margin=dict(l=0, r=0, b=0, t=0),
                showlegend=False,
                width=1000,
                height=1000,
                uirevision="keep",
            )
            figs.append(fig)
        return figs

    def plot_lon_lat_lines_plt(self, ax, n_latitudes, n_longitudes, theta, phi):
        # Longitude lines (meridians)
        r = 1.01
        for p in np.linspace(0, 2 * np.pi, n_latitudes):
            x_line = r * np.sin(theta) * np.cos(p)
            y_line = r * np.sin(theta) * np.sin(p)
            z_line = r * np.cos(theta)
            ax.plot(x_line, y_line, z_line, color="black", linewidth=0.5)

        # Latitude lines (parallels)
        for t in np.linspace(-np.pi / 2, np.pi / 2, n_longitudes):
            x_line = r * np.cos(t) * np.cos(phi)
            y_line = r * np.cos(t) * np.sin(phi)
            z_line = r * np.full_like(phi, np.sin(t))
            ax.plot(x_line, y_line, z_line, color="black", linewidth=0.5)

    def plot_coastline_plt(self, ax):
        coastline_data = self.get_coastline()
        r = 1.01
        for coords in coastline_data:
            lon, lat = coords
            lon = np.radians(lon)
            lat = np.radians(lat)
            x_coast = r * np.cos(lat) * np.cos(lon)
            y_coast = r * np.cos(lat) * np.sin(lon)
            z_coast = r * np.sin(lat)
            ax.plot(x_coast, y_coast, z_coast, color="black", linewidth=0.5)

    def plot_sphere_with_quiver(self, values=None):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_box_aspect([1, 1, 1])
        ax.axis("off")
        theta_grid, phi_grid = np.meshgrid(self.theta, self.phi)
        r = 0.9
        # Sphere grid
        x = r * np.sin(theta_grid) * np.cos(phi_grid)
        y = r * np.sin(theta_grid) * np.sin(phi_grid)
        z = r * np.cos(theta_grid)

        # White sphere
        ax.plot_surface(
            x, y, z, color="white", rstride=1, cstride=1, alpha=1, edgecolor="none"
        )

        # Lines & coast
        self.plot_lon_lat_lines_plt(
            ax, self.n_latitudes, self.n_longitudes, self.theta, self.phi
        )
        self.plot_coastline_plt(ax)

        if values is not None:
            # Quiver
            for xq, yq, zq, u, v, w in values:
                ax.quiver(
                    xq,
                    yq,
                    zq,
                    u,
                    v,
                    w,
                    length=0.1,
                    normalize=True,
                    color="blue",
                    linewidth=0.5,
                )

        plt.show()

    def export_frames(self, fig, folder="frames"):
        os.makedirs(folder, exist_ok=True)
        for i, frame in enumerate(fig.frames):
            fig.update(data=frame.data)
            pio.write_image(fig, f"{folder}/frame_{i:03d}.png", width=800, height=800)
        print(f"Exported {len(fig.frames)} frames to '{folder}/'")

    def render_video(self, folder="frames", output="out.mp4", speed=2):
        framerate = 20
        fast_filter = 1 / speed
        os.system(
            f"""
        ffmpeg -y -framerate {framerate} -i {folder}/frame_%03d.png -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p temp_out.mp4
        ffmpeg -y -i temp_out.mp4 -filter:v "setpts={fast_filter}*PTS" {output}
        rm temp_out.mp4
        """
        )
        print(f"Saved sped-up video as '{output}'")

    def save_figs(self, figs, folder="../images/rotating_earth"):
        os.makedirs(folder, exist_ok=True)
        for i, fig in enumerate(figs):
            pio.write_image(fig, f"{folder}/fig_{i:02d}.pdf", format="pdf", width=1000, height=1000)
        print(f"Saved {len(figs)} figures to '{folder}/'")