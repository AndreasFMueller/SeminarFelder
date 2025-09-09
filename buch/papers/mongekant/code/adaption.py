import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ot

reg = 1e-2
nb = 500
rng = np.random.RandomState(42)


def im2mat(img):
    """Converts and image to matrix (one pixel per line)"""
    return img.reshape((img.shape[0] * img.shape[1], img.shape[2]))


def mat2im(X, shape):
    """Converts back a matrix to an image"""
    return X.reshape(shape)


def minmax(img):
    return np.clip(img, 0, 1)


def imread(filename):
    return plt.imread(filename).astype(np.float64) / 256


def imsave(filename, img):
    """Save an image to a file"""
    Image.fromarray((img * 256).astype(np.uint8)).save(filename)


images = [
    imread("ocean_day.jpg"),
    imread("desert.jpg"),
    imread("jungle2.webp"),
]
n_images = len(images)

values = [im2mat(image) for image in images]

# training samples
idxs = [rng.randint(v.shape[0], size=(nb,)) for v in values]

outputs = np.empty((n_images, n_images), dtype=object)
for i in range(n_images):
    outputs[i][i] = images[i]
    for j in range(n_images):
        if i == j:
            continue

        source = values[i][idxs[i], :]
        target = values[j][idxs[j], :]

        ot_sinkhorn1 = ot.da.SinkhornTransport(reg_e=reg)
        ot_sinkhorn1.fit(Xs=source, Xt=target)
        transport_1 = ot_sinkhorn1.transform(Xs=values[i])
        sink1 = minmax(mat2im(transport_1, images[i].shape))

        ot_sinkhorn2 = ot.da.SinkhornTransport(reg_e=reg)
        ot_sinkhorn2.fit(Xs=target, Xt=source)
        transport2 = ot_sinkhorn2.transform(Xs=values[j])
        sink2 = minmax(mat2im(transport2, images[j].shape))

        imsave(f"{i}{j}.jpg", sink1)
        imsave(f"{j}{i}.jpg", sink2)
        outputs[i, j] = sink1
        outputs[j, i] = sink2

_, ax_mat = plt.subplots(n_images, n_images, constrained_layout=True)
for ax, out in zip(ax_mat.flatten(), outputs.flatten()):
    ax.axis("off")
    ax.imshow(out)

plt.show()
