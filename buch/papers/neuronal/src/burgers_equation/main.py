import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import qmc
from BurgersNet import BurgersNet
from Graphics import error_plot, solution_plot, snapshot_plot

matplotlib.use('TkAgg')
torch.set_default_dtype(torch.float64)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

### Model
model = BurgersNet().to(device)

### Training
if os.path.exists("burgers_net.pth"):
    model.load_state_dict(torch.load("burgers_net.pth"))
    print("Loaded trained model from file")
else:
    print("Training model...")
    train_error, test_error = model.fit(device, epochs=15000)
    torch.save(model.state_dict(), "burgers_net.pth")

    error_plot(train_error, test_error)

print("Model parameters:" + str(sum(p.numel() for p in model.parameters() if p.requires_grad))+"\n")

### Solution Plot
solution_plot(model, device)
snapshot_plot(model, device, t=0.8)
