import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import ot
import scipy.stats
import plotting

n_points = 201
n_pixels = 1001
step = 0.1
regularization = 1e-3
ratios = [1, 4]
gridspecs = {
    "width_ratios": ratios,
    "height_ratios": ratios,
    "wspace": 0.05,
    "hspace": 0.05,
}
plotting.init_book_style()


def plot_barycenters(x, alphas, bary_l2, bary_wasser, name, figsize=(5, 3)):
    # _, axs = plt.subplots(2, sharex=True, sharey=True, constrained_layout=True)
    fig_names = ["euclidean", "wasserstein"]
    legend_kwargs = {
        "frameon": False,
        "loc": "upper right",
        "handlelength": 1,
        "borderpad": 0.0,
    }
    fig1, ax1 = plt.subplots(constrained_layout=True, figsize=figsize)
    fig2, ax2 = plt.subplots(constrained_layout=True, figsize=figsize)
    fig3, ax3 = plt.subplots(constrained_layout=True, figsize=figsize)
    axs = (ax1, ax2)
    figs = (fig1, fig2)
    xlim = x[[0, -1]]
    ylim = (0, 1.05 * np.max(bary_l2))
    step = 2 * xlim[1]
    for fig, ax, p, fig_name in zip(figs, axs, [bary_l2, bary_wasser], fig_names):
        plotting.create_arrow_axis(step, 1, xlim, ylim, ax=ax, axisbelow=False)
        hues = 1 - alphas / 3
        hsvs = np.stack((hues, np.ones_like(hues), np.ones_like(hues)), axis=-1)
        colors = mcolors.hsv_to_rgb(hsvs)
        for pi, c, w in zip(p.T, colors, alphas):
            alpha = 1 if np.isclose(w % 1, 0) else 0.4
            ax.plot(x, pi, color=c, alpha=alpha)

    plotting.create_arrow_axis(step, 1, xlim, ylim, ax=ax3, axisbelow=False)
    ax3.plot(x, p[:, 0], color=colors[0], label="$\\mu$")
    ax3.plot(x, p[:, -1], color=colors[-1], label="$\\nu$")
    ax3.legend(**legend_kwargs)
    fig3.savefig(f"barycenter_{name}_init.pdf")

    for ax in axs:
        ax.legend([f"$\\rho(\\alpha = {w:.1f})$" for w in alphas], **legend_kwargs)
    for fig, fig_name in zip((fig1, fig2), fig_names):
        fig.savefig(f"barycenter_{name}_{fig_name}.pdf")
    return figs, axs


def compute_barycenters(ab, dist, alphas, reg=1e-3):
    weights = np.stack((1 - alphas, alphas), axis=1)
    bary_l2 = (ab[:, None] * weights[None]).sum(axis=-1)
    bary_wasser = np.empty_like(bary_l2)
    for i in range(len(alphas)):
        bary_wasser[:, i] = ot.bregman.barycenter(
            ab, dist, reg, weights[i], method="sinkhorn"
        )
    bary_wasser[:, 0] = ab[:, 0]
    bary_wasser[:, -1] = ab[:, 1]
    return bary_l2, bary_wasser


def plot_ot(x, a, b, dist, index, reg=1e-3, figsize=(2.8, 2.8)):
    ot_map = ot.sinkhorn(a, b, dist, reg=reg, numItermax=1000)

    fig, axs = plt.subplots(
        2,
        2,
        sharex="col",
        sharey="row",
        gridspec_kw=gridspecs,
        constrained_layout=True,
        figsize=figsize,
    )
    for _ax in axs.flatten():
        _ax.axis("off")
    axs[0, 1].fill_between(x, b, color="blue", alpha=0.5)
    axs[0, 1].plot(x, b, color="blue", label="$\\boldsymbol\\nu$")
    axs[0, 1].legend(
        frameon=False,
        handlelength=0,
        fontsize="x-large",
        labelcolor="blue",
        loc="upper center",
    )
    axs[1, 0].fill_betweenx(x, -a, color="red", alpha=0.5)
    axs[1, 0].plot(-a, x, color="red", label="$\\boldsymbol\\mu$")
    axs[1, 0].legend(
        frameon=False,
        handlelength=0,
        fontsize="x-large",
        labelcolor="red",
        loc="center",
    )
    axs[1, 1].imshow(ot_map, cmap="gray", interpolation="nearest", label="$\\gamma")
    axs[1, 1].text(
        0.9,
        0.9,
        "$\\boldsymbol\\gamma$",
        color="white",
        fontsize="x-large",
        transform=axs[1, 1].transAxes,
    )
    fig.savefig(f"ot_map_{index}.pdf")


alphas = np.arange(0, 1 + 0.5 * step, step)
sigma = 0.08 * n_points
x = np.arange(n_points, dtype=np.float64)

a = scipy.stats.norm(loc=0.65 * n_points, scale=sigma).pdf(x)
a /= a.sum()
b = scipy.stats.rayleigh(loc=0, scale=0.1 * n_points).pdf(x)
b /= b.sum()
b2 = scipy.stats.norm(loc=0.25 * n_points, scale=0.5 * sigma).pdf(x)
b2 += scipy.stats.norm(loc=0.75 * n_points, scale=0.5 * sigma).pdf(x)
b2 /= b2.sum()

# Compute the cost matrix
_x = x[:, None]
dist = ot.dist(_x, _x, "sqeuclidean")
dist /= dist.max()

ab = np.stack((a, b), axis=1)
ab2 = np.stack((a, b2), axis=1)
be1, bw1 = compute_barycenters(ab, dist, alphas, regularization)
be2, bw2 = compute_barycenters(ab2, dist, alphas, regularization)
plot_barycenters(x, alphas, be1, bw1, "ray")
plot_barycenters(x, alphas, be2, bw2, "bi")

# Create the distributions for the OT example
sigma = 0.15 * n_pixels
x = np.arange(n_pixels, dtype=np.float64)
a = scipy.stats.norm(loc=n_pixels // 2, scale=sigma).pdf(x)
a /= a.sum()
b = scipy.stats.rayleigh(loc=0, scale=0.2 * n_pixels).pdf(x)
b /= b.sum()
b2 = scipy.stats.norm(loc=0.25 * n_pixels, scale=0.5 * sigma).pdf(x)
b2 += scipy.stats.norm(loc=0.75 * n_pixels, scale=0.5 * sigma).pdf(x)
b2 /= b2.sum()

# Compute the cost matrix
_x = x[:, None]
dist = ot.dist(_x, _x)
dist /= dist.max()

plot_ot(x, a, b, dist, 1)
plot_ot(x, a, b2, dist, 2)
