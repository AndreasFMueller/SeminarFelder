import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import Normalize, PowerNorm
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
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

# --- physics and helpers (same as before) ---
g, R, kappa = 9.80665, 287.0, 1.4
KR = kappa * R
X_LIM = 22000
MACH_LIST   = [1.05, 1.1, 1.50, 2.50]
LINESTYLES  = ['-.', '--', '-', ':']


def p_of_T(z, Tz, p0=101325.0):
    z = np.asarray(z); Tz = np.asarray(Tz)
    ln_p = np.zeros_like(z, dtype=float)
    for i in range(1, len(z)):
        dz = z[i]-z[i-1]
        Tm = 0.5*(Tz[i]+Tz[i-1])
        ln_p[i] = ln_p[i-1] - g*dz/(R*Tm)
    return p0*np.exp(ln_p)

def c_from_T(Tz): return np.sqrt(KR*Tz)

def integrate_ray(z_a, V, c_of_z, z_min=0.0, n_steps=6000):
    """
    Integriert den Machrand x(z) von z_a abwärts bis z_min mit
    dx/dz = (c/V) / sqrt(1 - (c/V)^2) = 1 / sqrt(V^2/c^2 - 1).

    Rückgabe:
      z : absteigendes z-Gitter (inkl. letzter gültiger Punkt)
      x_right : x(z) für den rechten Rand (x >= 0)
      x_left  : x(z) für den linken Rand  (x <= 0), symmetrisch zu x_right
    """
    # z-Gitter (abwärts)
    z = np.linspace(z_a, z_min, n_steps)
    cz = c_of_z(z)

    # Radikand für dx/dz:  V^2/c^2 - 1  (nur strikt positive Werte zulassen)
    rad = (V / cz)**2 - 1.0
    valid = rad > 0.0
    if not np.any(valid):
        # kein realer Strahl (V <= c überall)
        return z[:1], np.array([0.0]), np.array([0.0])

    # nur bis zum letzten Punkt gehen, an dem der Strahl noch reell ist
    last_ok = np.nonzero(valid)[0][-1]
    z = z[:last_ok + 1]
    rad = rad[:last_ok + 1]

    # Integrand: dx/dz
    dxdz = 1.0 / np.sqrt(rad)

    # Trapezregel über z (Achtung: z nimmt ab, daher -dz)
    dz = np.diff(z)                     # negative Werte
    x = np.zeros_like(z)
    if len(z) > 1:
        x[1:] = np.cumsum(0.5 * (dxdz[1:] + dxdz[:-1]) * (-dz))

    # Symmetrische Ränder: rechts (+x), links (-x)
    return z, x, -x

# --- scenarios ---
z_a = 3500.0
z_ref, T_ref = 1500.0, 285.0
L_mag = 0.0090
L_norm, L_inv = -L_mag, +L_mag
T0_norm, T0_inv = T_ref - L_norm*z_ref, T_ref - L_inv*z_ref
T_norm = lambda z: T0_norm + L_norm*z
T_inv  = lambda z: T0_inv  + L_inv*z
c_normf = lambda z: c_from_T(T_norm(z))
c_invf  = lambda z: c_from_T(T_inv(z))
M_common = 1.05
V_norm = M_common * c_normf(z_a)
V_inv  = M_common * c_invf(z_a)

# global ranges
z_side = np.linspace(0.0, 5000.0, 800)
Tn, Ti = T_norm(z_side), T_inv(z_side)
pn, pi = p_of_T(z_side, Tn), p_of_T(z_side, Ti)
rho_n, rho_i = pn/(R*Tn), pi/(R*Ti)
c_n, c_i     = c_from_T(Tn), c_from_T(Ti)
RHO_MIN, RHO_MAX = float(min(rho_n.min(), rho_i.min())), float(max(rho_n.max(), rho_i.max()))
C_MIN,   C_MAX   = float(min(c_n.min(),   c_i.min()  )), float(max(c_n.max(),   c_i.max()  ))
T_MIN,   T_MAX   = float(min(Tn.min(),    Ti.min()   )), float(max(Tn.max(),    Ti.max()   ))

rho_norm = PowerNorm(gamma=0.7, vmin=RHO_MIN, vmax=RHO_MAX)
c_norm   = Normalize(vmin=C_MIN, vmax=C_MAX)

rho_norm = PowerNorm(gamma=0.7, vmin=RHO_MIN, vmax=RHO_MAX)
c_norm   = Normalize(vmin=C_MIN, vmax=C_MAX)
T_norm_m = Normalize(vmin=T_MIN, vmax=T_MAX)

def paint_density_gray(ax, z_max, x_halfspan, T_of_z, alpha=0.10):
    z = np.linspace(0, z_max, 600); Tz = T_of_z(z)
    rho = p_of_T(z, Tz)/(R*Tz); img = np.tile(rho.reshape(-1,1), (1, 320))
    ax.imshow(img, origin='lower', extent=(-x_halfspan, x_halfspan, 0, z_max),
              cmap='Greys', norm=rho_norm, alpha=alpha, aspect='auto', zorder=0)

def paint_temperature_red(ax, z_max, x_halfspan, T_of_z, alpha=0.22):
    z = np.linspace(0, z_max, 600); Tz = T_of_z(z)
    img = np.tile(Tz.reshape(-1,1), (1, 320))
    ax.imshow(img, origin='lower', extent=(-x_halfspan, x_halfspan, 0, z_max),
              cmap='Reds', norm=T_norm_m, alpha=alpha, aspect='auto', zorder=1)

def _right_edge_positions(cs, ax, levels_to_label=None, margin_frac=0.02):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    xm = x1 - margin_frac * (x1 - x0)

    if levels_to_label is None:
        levels_to_label = list(cs.levels)

    lvl_to_idx = {lvl: i for i, lvl in enumerate(cs.levels)}

    levels_ok = []
    pos_ok = []

    for lvl in levels_to_label:
        i = lvl_to_idx.get(lvl, None)
        if i is None:
            continue
        segments = cs.allsegs[i]  # list of (N,2) arrays; may be empty

        # find crossings with x = xm
        ys = []
        for seg in segments:
            if len(seg) < 2:
                continue
            x = seg[:, 0]; y = seg[:, 1]
            xi, xj = x[:-1], x[1:]
            yi, yj = y[:-1], y[1:]
            crosses = (xi - xm) * (xj - xm) <= 0
            idx = np.nonzero(crosses)[0]
            for k in idx:
                if xj[k] != xi[k]:
                    t = (xm - xi[k]) / (xj[k] - xi[k])
                    yc = yi[k] + t * (yj[k] - yi[k])
                    if y0 <= yc <= y1:
                        ys.append(yc)

        if ys:
            yc = min(ys, key=lambda yy: abs(yy - 0.5*(y0+y1)))
            levels_ok.append(lvl)
            pos_ok.append((xm, yc))
        else:
            # fallback: pick the point with the largest x among all segments
            best_x, best_y = -np.inf, None
            for seg in segments:
                if len(seg):
                    j = np.argmax(seg[:, 0])
                    if seg[j, 0] > best_x:
                        best_x, best_y = seg[j, 0], seg[j, 1]
            if best_y is not None:
                levels_ok.append(lvl)
                pos_ok.append((min(best_x, xm), best_y))

    return levels_ok, pos_ok

def draw_c_isolines_every_5(ax, z_max, x_halfspan, T_of_z):
    nx, nz = 360, 720
    x = np.linspace(-x_halfspan, x_halfspan, nx)
    z = np.linspace(0, z_max, nz)
    X, Z = np.meshgrid(x, z)
    c = c_from_T(T_of_z(Z))

    start = int(np.ceil(C_MIN/5.0)*5)
    stop  = int(np.floor(C_MAX/5.0)*5)
    levels = np.arange(start, stop+1, 5)

    cs = ax.contour(X, Z, c, levels=levels,
                    colors=['midnightblue'], linewidths=1.1, zorder=3)

    # Fix limits before computing positions
    ax.set_xlim(-x_halfspan, x_halfspan)
    ax.set_ylim(0, z_max)

    levels_lbl = levels[::2]  # your choice
    levels_ok, pos_ok = _right_edge_positions(cs, ax, levels_to_label=levels_lbl, margin_frac=0.04)

    if pos_ok:
        for lvl, (xlab, ylab) in zip(levels_ok, pos_ok):
            ax.text(
                float(xlab), float(ylab), f"{int(lvl)}",
                va="center", ha="left",
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.1),
                path_effects=[pe.withStroke(linewidth=4, foreground="white")],  # crisp on top of lines
                zorder=5
    )
    else:
        # fallback: let matplotlib choose positions (still restrict levels)
        ax.clabel(cs, levels=levels_lbl, inline=True, fontsize=10, fmt='%d', colors='midnightblue')


def add_three_cbars(fig, axR):
    """Stack three colorbars on far right: top=c, mid=T, bottom=rho."""
    box = axR.get_position()
    pad = 0.012; width = 0.018
    height_each = (box.height - 4*pad) / 3.0
    # bottom: rho
    cax_rho = fig.add_axes([box.x1 + pad, box.y0 + pad, width, height_each])
    sm_rho = mpl.cm.ScalarMappable(norm=rho_norm, cmap='Greys'); sm_rho.set_array([])
    cb_rho = fig.colorbar(sm_rho, cax=cax_rho); cb_rho.set_label(r"$\rho$ (kg m$^{-3}$)", fontsize=14)
    # mid: T
    cax_T = fig.add_axes([box.x1 + pad, box.y0 + 2*pad + height_each, width, height_each])
    sm_T = mpl.cm.ScalarMappable(norm=T_norm_m, cmap='Reds'); sm_T.set_array([])
    cb_T = fig.colorbar(sm_T, cax=cax_T); cb_T.set_label(r"$T$ (K)", fontsize=14)
    # top: c
    cax_c = fig.add_axes([box.x1 + pad, box.y0 + 3*pad + 2*height_each, width, height_each])
    sm_c = mpl.cm.ScalarMappable(norm=c_norm, cmap='Blues'); sm_c.set_array([])
    cb_c = fig.colorbar(sm_c, cax=cax_c); cb_c.set_label(r"$c$ (m s$^{-1}$)", fontsize=14)
    return cb_c, cb_T, cb_rho


def side_strip(ax, z, field, cmap, norm, title, show_yticks):
    tile = np.tile(field.reshape(-1,1), (1, 12))
    ax.imshow(tile, origin='lower', extent=(0, 1, z.min(), z.max()),
              cmap=cmap, norm=norm, aspect='auto', zorder=0)
    ax.set_xlim(0, 1); ax.set_ylim(z.min(), z.max()); ax.set_xticks([])
    ax.set_title(title, fontsize=14)
    ax.grid(True, axis='y', alpha=0.2)
    if show_yticks:
        ax.set_ylabel(r"$z$ (m)", fontsize=14)
        ax.set_yticks(np.arange(0, 5001, 500))
    else:
        ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        ax.set_ylabel("")

def build_panel(title, T_of_z, c_of_z, ray_color, out_file):
    fig = plt.figure(figsize=(10.4, 5.8))
    gs = GridSpec(1, 3, width_ratios=[0.5, 7.0, 0.5], wspace=0.05, figure=fig)
    axL = fig.add_subplot(gs[0,0])
    ax  = fig.add_subplot(gs[0,1], sharey=axL)
    axR = fig.add_subplot(gs[0,2], sharey=axL)

    # main
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim([-X_LIM, X_LIM]); ax.set_ylim([0, 5000])
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("$x$ (m)", fontsize=14)
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    ax.set_title(title, fontsize=16)

    x_half = X_LIM
    # paint_density_gray(ax, 5000, x_half, T_of_z, alpha=0.70)
    paint_temperature_red(ax, 5000, x_half, T_of_z, alpha=0.8)
    draw_c_isolines_every_5(ax, 5000, x_half, T_of_z)

    # kleine Hintergrundlegende für Felder
    sw_rho = mpl.patches.Patch(facecolor='0.2', alpha=0.10, edgecolor='none', label=r'Dichte $\rho$')
    sw_T   = mpl.patches.Patch(facecolor='red',  alpha=0.22, edgecolor='none', label=r'Temperatur $T$')
    sw_c   = mpl.lines.Line2D([0],[0], color='midnightblue', lw=1.4, label=r'Schallgeschw. $c$')
    leg = ax.legend(handles=[sw_rho, sw_T, sw_c], loc=(0.243, 0.78), frameon=True, framealpha=1.0, fontsize=14)
    leg.get_frame().set_edgecolor((0,0,0,0.25)); ax.add_artist(leg)

    # Flugzeug
    ax.axhline(0.0, color='k', lw=1.0)
    ax.plot([0],[z_a], 'ko', ms=4); ax.annotate("Flugzeug $z_a$", (0, z_a), xytext=(6,2), textcoords='offset points', fontsize=14)

    # Strahlen für drei Machzahlen (Linienstil kodiert Mach)
    for Ma, ls in zip(MACH_LIST, LINESTYLES):
        V = Ma * c_of_z(z_a)
        z, xr, xl = integrate_ray(z_a, V, c_of_z)
        lbl = fr"Ma = {Ma:.2f}"
        ax.plot(xr, z, lw=2.6, color=ray_color, linestyle=ls, label=lbl)
        ax.plot(xl, z, lw=2.6, color=ray_color, linestyle=ls)

    # Legende nur mit Mach-Linienstilen (Farben sind szenario-spezifisch)
    ma_leg = ax.legend(loc='upper left', frameon=True, framealpha=1.0,  fontsize=14,
                       title=r"Machzahl $\textit{Ma}$", title_fontsize=14)
    ma_leg.get_frame().set_edgecolor((0,0,0,0.25)); ax.add_artist(ma_leg)

    # custom Legende mit Temperaturen
    textstr = rf"$\begin{{array}}{{rcl}} T({z_a:.0f}) & = & {T_of_z(z_a):.1f}\,\mathrm{{K}}\\[0.45ex]T({z_ref:.0f}) & = & {T_of_z(z_ref):.1f}\,\mathrm{{K}}\\[0.45ex]T(0) & = & {T_of_z(0):.1f}\,\mathrm{{K}} \end{{array}}$"
    props = dict(boxstyle='round', facecolor='white', alpha=1.0)
    ax.text(0.543, 0.965, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    # side strips
    rho = p_of_T(z_side, T_of_z(z_side))/(R*T_of_z(z_side))
    csp = c_from_T(T_of_z(z_side))
    side_strip(axL, z_side, rho, "Greys", rho_norm, r"$\rho(z)$", show_yticks=True)
    side_strip(axR, z_side, csp, "Blues", c_norm, r"$c(z)$", show_yticks=False)

    # drei Colorbars rechts
    add_three_cbars(fig, axR)

    fig.tight_layout()
    fig.savefig(out_file.with_suffix('.png'), dpi=600)
    fig.savefig(out_file.with_suffix('.pdf'), dpi=600)
    plt.close(fig)


def build_overlay(z_a, c_normf, c_invf, out_file):
    fig = plt.figure(figsize=(10.4, 5))
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('auto', adjustable='box')
    ax.set_xlim([-X_LIM, X_LIM]); ax.set_ylim([0, 4000])
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("$x$ (m)", fontsize=14)
    ax.set_ylabel("$z$ (m)", fontsize=14)
    ax.set_title("Direkter Vergleich: Normale Lage vs. Inversion", fontsize=16)

    # Flugzeug
    ax.axhline(0.0, color='k', lw=1.0)
    ax.plot([0],[z_a], 'ko', ms=4)
    ax.annotate("Flugzeug $z_a$", (0, z_a), xytext=(6,4), textcoords='offset points', fontsize=14)

    # Farben: blau = normal, grün = inversion; Linienstil = Mach
    color_norm = "#1f77b4"
    color_inv  = "#2ca02c"

    handles = []
    # kurzes Hilfsobjekt für Legenden-Keys (nur Linienstil/Mach)
    for Ma, ls in zip(MACH_LIST, LINESTYLES):
        h = mpl.lines.Line2D([0],[0], color='k', linestyle=ls, lw=2.0, label=fr"Ma={Ma:.2f}")
        handles.append(h)

    # Rays für jede Machzahl in beiden Szenarien
    for Ma, ls in zip(MACH_LIST, LINESTYLES):
        Vn = Ma * c_normf(z_a)
        Vi = Ma * c_invf(z_a)
        zN, xNr, xNl = integrate_ray(z_a, Vn, c_normf)
        zI, xIr, xIl = integrate_ray(z_a, Vi, c_invf)
        ax.plot(xNr, zN, lw=2.6, color=color_norm, linestyle=ls, label=None)
        ax.plot(xNl, zN, lw=2.6, color=color_norm, linestyle=ls, label=None)
        ax.plot(xIr, zI, lw=2.6, color=color_inv,  linestyle=ls, label=None)
        ax.plot(xIl, zI, lw=2.6, color=color_inv,  linestyle=ls, label=None)

    # Doppelte Legende: oben links (Szenario-Farben), oben rechts (Mach-Linienstile)
    leg1 = ax.legend(handles=[
            mpl.lines.Line2D([0],[0], color=color_norm, lw=3, label="Normale Lage"),
            mpl.lines.Line2D([0],[0], color=color_inv,  lw=3, label="Inversionslage")],
            loc="upper left", frameon=True, framealpha=1.0, fontsize=14,
            title="Szenario", title_fontsize=14)
    ax.add_artist(leg1)
    ax.legend(handles=handles, loc="upper right", frameon=True, framealpha=1.0, fontsize=14,
              title=r"Machzahl $\textit{Ma}$", title_fontsize=14)

    fig.tight_layout()
    fig.savefig(out_file.with_suffix('.png'), dpi=600)
    fig.savefig(out_file.with_suffix('.pdf'), dpi=600)
    plt.close(fig)


out_dir = Path("../figures")
out_dir.mkdir(parents=True, exist_ok=True)
# build two figures
build_panel(r"Normale Lage: $T(z) = T_0 - Lz$",
            T_norm, c_normf, "#1f77b4",
            out_dir/"normal_sidepanels")

build_panel(r"Inversionslage: $T(z) = T_0 + L_Iz$",
            T_inv, c_invf, "#2ca02c",
            out_dir/"inversion_sidepanels")

build_overlay(z_a, c_normf, c_invf,
            out_dir/"overlay_clean")
