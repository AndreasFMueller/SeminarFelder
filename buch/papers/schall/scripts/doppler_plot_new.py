import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams['text.usetex'] = True

mpl.rcParams.update({
    "text.usetex": True,                       # use LaTeX
    "font.family": "serif",                    # serif family (Times-like)
    "text.latex.preamble": r"""
        \usepackage[T1]{fontenc}
        \usepackage{amsmath}
        \usepackage{txfonts}
    """,
})

CONFIG = {
    "c": 343.0,
    "t_final": 1.0,
    "emit_dt": 0.20,
    "circle_alpha": 0.9,
    "circle_lw": 1.3,
    "dpi": 600,
    "figsize": (12, 4.4),
    "axis_padding_frac": 0.08,
    "right_pad_frac": 0.05,       # extra pad on right to keep arrows fully visible
    "v_sub_frac": 0.6,
    "M_sup": 1.7,
    "out_dir": "../figues",
    "wspace": -0.45,
    "title_y": 0.96,
    "title_offsets": [-220, -320, -350],  # per panel (sub, sonic, sup) in data x-units
}

out_dir = Path(CONFIG["out_dir"])
out_dir.mkdir(parents=True, exist_ok=True)

def emission_times(t_end, dt):
    n = int(np.floor(t_end / dt))
    return np.linspace(0.0, n * dt, n + 1)

def circle_points(center, radius, n=240):
    theta = np.linspace(0, 2*np.pi, n)
    cx = center[0] + radius * np.cos(theta)
    cy = center[1] + radius * np.sin(theta)
    return cx, cy

def scenario_geometry(c, t, emit_dt, mode, v_sub_frac=None, M_sup=None):
    taus = emission_times(t, emit_dt)
    if mode == "sub":
        v = v_sub_frac * c
    elif mode == "sonic":
        v = c
    elif mode == "sup":
        v = M_sup * c
    else:
        raise ValueError("mode must be 'sub', 'sonic', or 'sup'")
    centers = np.column_stack((v * taus, np.zeros_like(taus)))
    radii = c * (t - taus)
    centers = centers[:-1]
    radii = radii[:-1]
    info = {"centers": centers, "radii": radii, "v": v, "mode": mode}
    if mode == "sonic":
        info["envelope_x"] = v * t
    if mode == "sup":
        info["mu"] = np.arcsin(1.0 / (v / c))
        info["x_src"] = v * t
    return info

def global_limits_with_arrows(geoms, padding_frac, right_pad_frac, c, t):
    # Include circles + arrow endpoints + special features in bounds
    xs_all = []
    ys_all = []
    for g in geoms:
        for center, r in zip(g["centers"], g["radii"]):
            cx, cy = circle_points(center, r, n=72)
            xs_all.append(cx); ys_all.append(cy)
        # arrow end at 1.2 * v*t
        x_end = 1.2 * g["v"] * t
        xs_all.append(np.array([0.0, x_end]))
        ys_all.append(np.array([0.0, 0.0]))
        # sonic envelope / supersonic apex
        if g["mode"] == "sonic":
            xs_all.append(np.array([g["envelope_x"]]))
            ys_all.append(np.array([0.0]))
        if g["mode"] == "sup":
            xs_all.append(np.array([g["x_src"]]))
            ys_all.append(np.array([0.0]))
    xs = np.concatenate(xs_all) if len(xs_all) else np.array([0.0])
    ys = np.concatenate(ys_all) if len(ys_all) else np.array([0.0])
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    span = max(x_max - x_min, y_max - y_min, 1.0)
    pad = padding_frac * span
    # make square box
    x_mid = 0.5 * (x_min + x_max)
    y_mid = 0.5 * (y_min + y_max)
    half = 0.5 * span + pad
    xmin = x_mid - half
    xmax = x_mid + half
    ymin = y_mid - half
    ymax = y_mid + half
    # extra right pad for arrows
    extra = right_pad_frac * span
    xmax += extra
    return xmin+80, xmax, ymin, ymax

def draw_panel(ax, geom, limits, c, t, title_text, title_offset):
    xmin, xmax, ymin, ymax = limits
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.axis('off')

    cycle_colors = [d['color'] for d in plt.rcParams['axes.prop_cycle']]
    num = len(geom["radii"])
    colors = cycle_colors * (num // len(cycle_colors) + 1)
    colors = colors[:num]

    for (center, r), col in zip(zip(geom["centers"], geom["radii"]), colors):
        cx, cy = circle_points(center, r, n=240)
        ax.plot(cx, cy, linewidth=CONFIG["circle_lw"], alpha=CONFIG["circle_alpha"], color=col)
        ax.plot([center[0]], [center[1]], marker="o", color=col, markersize=4)

    # arrow from (0,0) to 1.2*(v*t, 0)
    v = geom["v"]
    x_end = 1.25 * v * t
    span_x = xmax - xmin
    span_y = ymax - ymin
    ax.arrow(0, 0, x_end, 0,
             head_width=0.035*span_y, head_length=0.05*span_x,
             fc='black', ec='black', linewidth=1.2, length_includes_head=True)

    if geom["mode"] == "sonic":
        x_src = geom["envelope_x"]
        ax.plot([x_src, x_src], [ymin+100, ymax-100], linewidth=1.5, color="black")
        x_title = x_src
    elif geom["mode"] == "sup":
        mu = geom["mu"]
        x_src = geom["x_src"]
        L = (xmax - xmin)
        xs = np.linspace(x_src - L + 500, x_src, 200)
        ys = (x_src - xs) * np.tan(mu)
        ax.plot(xs, ys, linewidth=1.6, color="black")
        ax.plot(xs, -ys, linewidth=1.6, color="black")
        ax.text(x_src - 0.25*L, 0.32*L*np.tan(mu),
                r"$\mu=\sin^{-1}(\frac{1}{\textit{Ma}})$", fontsize=22, color="black")
        x_title = x_src
    else:
        x_title = v * t

    # Title centered over x_title plus custom offset (in data units)
    x_title_adj = x_title + title_offset
    x_rel = (x_title_adj - xmin) / (xmax - xmin) if xmax > xmin else 0.5
    ax.text(x_rel, CONFIG["title_y"], title_text,
            transform=ax.transAxes, ha="center", va="bottom", fontsize=22)

# Build data
c = CONFIG["c"]; t = CONFIG["t_final"]; dt = CONFIG["emit_dt"]
geom_sub   = scenario_geometry(c, t, dt, mode="sub",  v_sub_frac=CONFIG["v_sub_frac"])
geom_sonic = scenario_geometry(c, t, dt, mode="sonic")
geom_sup   = scenario_geometry(c, t, dt, mode="sup",  M_sup=CONFIG["M_sup"])

# Identical limits that also include arrow endpoints and extra right pad
limits = global_limits_with_arrows([geom_sub, geom_sonic, geom_sup],
                                   CONFIG["axis_padding_frac"],
                                   CONFIG["right_pad_frac"], c, t)

# Figure
fig, axes = plt.subplots(1, 3, figsize=CONFIG["figsize"])
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.06, top=0.92, wspace=CONFIG["wspace"])

title_offsets = CONFIG["title_offsets"]
draw_panel(axes[0], geom_sub,   limits, c, t, r"$\textit{Ma} < c$", title_offsets[0])
draw_panel(axes[1], geom_sonic, limits, c, t, r"$\textit{Ma} = c$", title_offsets[1])
draw_panel(axes[2], geom_sup,   limits, c, t, r"$\textit{Ma} > c$", title_offsets[2])

png_path = out_dir / "mach_doppler_triptych_offsets.png"
svg_path = out_dir / "mach_doppler_triptych_offsets.pdf"
fig.savefig(png_path, dpi=CONFIG["dpi"])
fig.savefig(svg_path)
plt.close(fig)

(png_path.as_posix(), svg_path.as_posix())
