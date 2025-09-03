import matplotlib.pyplot as plt
import ot
import numpy as np
import plotting


plotting.init_book_style()
reg = 6e-4
n_steps = 6


def interpolate_wasserstein(data, alphas):
    outputs = np.empty((len(alphas), *data[0].shape), dtype=np.float64)
    for i, alpha in enumerate(alphas):
        if (alpha % 1) == 0:
            outputs[i] = data[alpha.astype(int)]
            continue
        weights = np.array([1 - alpha, alpha])
        outputs[i] = ot.bregman.convolutional_barycenter2d(data, reg, weights)
    return outputs


def interpolate_euclidean(data, alphas):
    weights = np.stack((1 - alphas, alphas), axis=0)
    outputs = np.sum(data[:, None] * weights[:, :, None, None], axis=0)
    return outputs


def plot_outputs(outputs, figsize=(n_steps, 1)):
    fig, axs = plt.subplots(1, n_steps, constrained_layout=True, figsize=figsize)
    for ax, out in zip(axs, outputs):
        ax.imshow(out, cmap="gray")
        ax.axis("off")
    return fig, axs


alphas = np.linspace(0, 1, n_steps)
one = plt.imread("one.bmp").astype(np.float64) / 256
one /= one.sum()
eight = plt.imread("eight.bmp").astype(np.float64) / 256
eight /= eight.sum()
data = np.array([one, eight])

outputs_wasser = interpolate_wasserstein(data, alphas)
fig1, _ = plot_outputs(outputs_wasser)
outputs_euclid = interpolate_euclidean(data, alphas)
fig2, _ = plot_outputs(outputs_euclid)
fig1.savefig("wasserstein2d.pdf")
fig2.savefig("euclidean2d.pdf")
