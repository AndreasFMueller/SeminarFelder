import numpy as np
from plot_dgl import RechargeOscillator
from enable_export import enable_export

enable_export()

# RechargeOscillator
alpha = 1 / 8
epsilon = 0.1
b = 2
gamma = 3 / 4
r = 1 / 4

nullx = - (
    r
    * np.sqrt(alpha * b * gamma - b * gamma * r + r)
    / (np.sqrt(epsilon) * np.sqrt(b**3 * (alpha - r) ** 3))
)
nullx = 0
nully = - alpha * b * nullx / r

ro = RechargeOscillator(alpha, epsilon, b, gamma, r)
print(ro.run(1000, [nullx, nully]))

# Nullklinen example

