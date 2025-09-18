import numpy as np
from plot import Plot_Sphere
import plotly.graph_objects as go
from dash_app import dash_app
from rossby import random_field, vorticity_field, zonal_jet_field, rossby_wave_field


def plot_basic_sphere():

    n_latitudes = 50
    n_longitudes = 50
    pole_margin = 0
    theta = np.linspace(
        np.deg2rad(pole_margin), np.deg2rad(180 - pole_margin), n_latitudes
    )
    phi = np.linspace(0, 2 * np.pi, n_longitudes, endpoint=True)  # Longitude angles
    plot_sphere = Plot_Sphere(
        theta=theta,
        phi=phi,
        fields=None,
        plot_coastlines=True,
        plot_lonlat_lines=True,
        stride_latitudes=5,
        stride_longitudes=5,
    )

    # values = zonal_jet_field(theta=theta, phi=phi)
    # plot_sphere.plot_sphere_with_quiver(None)
    traces = plot_sphere.plot_sphere()
    # fig = plot_sphere.make_fig(traces)
    figs = plot_sphere.make_rotating_figs(traces, n=32)
    # figs = [fig]
    plot_sphere.save_figs(figs)
    # app = dash_app(figs)
    # app.run(debug=True)



    # t = np.linspace(0, 10, 50)
    # values = vorticity_field(theta=theta, phi=phi, t=t)
    # values = rossby_wave_field(theta=theta, phi=phi, t=t)

    # figs = plot_sphere.streamline(values)
    # traces = plot_sphere.streamtube_plot(values)
    # sphere_plot = plot_sphere.plot_sphere()
    # traces = plot_sphere.plot_sphere_surface(values)
    # traces = plot_sphere.rossby_surface_with_flow(values)
    # figs = []
    # fig = plot_sphere.animate_sphere(
    #     static_traces=[], changing_traces=traces
    # )
    # figs = [fig]
    # for cone_plot in cone_plots:
    #     fig = plot_sphere.make_fig([cone_plot] + sphere_plot)
    #     figs.append(fig)
    # app = dash_app(figs)
    # app.run(debug=True)

    # fields = random_field(theta, phi)

    # plot_sphere.rotating_sphere()
    # figs = plot_sphere.animate_sphere_multiple_figs()

    # fig = plot_sphere.animate_sphere()
    # figs = [fig]
    # traces = plot_sphere(
    #     theta, phi, field=None, plot_coastlines=True, plot_lonlat_lines=True
    # )
    # fig = make_fig(traces)
    # # Show plot
    # app = dash_app(figs)
    # app.run(debug=True)


if __name__ == "__main__":
    plot_basic_sphere()
