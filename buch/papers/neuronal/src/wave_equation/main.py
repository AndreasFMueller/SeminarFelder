import os
import boundaries
import torch
from WaveNet import WaveNet
from Graphics import *
matplotlib.use('TkAgg')


# Training setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = WaveNet().to(device)
print("Model parameters: " + str(sum(p.numel() for p in model.parameters() if p.requires_grad)) + "\n")

if os.path.exists("wavenet.pth"):
    model.load_state_dict(torch.load("wavenet.pth", map_location=device))
    model.eval()
    print("Loaded trained model from file\n")
else:
    print("Training model...")
    # Generate training & testing points
    n_train = 40000
    n_test = 10000
    # Train: x in (-1.5,2], y in [-2, 1.5] and t in [0, 1.5] --> Test: x in [-2, -1.5], y in (1.5 ,2] and t in (1.5, 2]
    x_train = torch.FloatTensor(n_train, 1).uniform_(boundaries.X_MIN + 0.5, boundaries.X_MAX)
    y_train = torch.FloatTensor(n_train, 1).uniform_(boundaries.Y_MIN, boundaries.Y_MAX - 0.5)
    t_train = torch.FloatTensor(n_train, 1).uniform_(boundaries.T_MIN, boundaries.T_MAX - 0.5)

    x_test = torch.FloatTensor(n_test, 1).uniform_(boundaries.X_MIN, boundaries.X_MIN + 0.5)
    y_test = torch.FloatTensor(n_test, 1).uniform_(boundaries.Y_MAX - 0.5, boundaries.Y_MAX)
    t_test = torch.FloatTensor(n_test, 1).uniform_(boundaries.T_MAX - 0.5, boundaries.T_MAX)

    train_error, test_error = model.fit(x_train, y_train, t_train, x_test, y_test, t_test, device, n_epochs=1500)
    torch.save(model.state_dict(), "wavenet.pth")
    print("\nModel saved to 'wavenet.pth'\n")

    error_plot(train_error, test_error)
    model.eval()

# Animation
animate_comparison(model, device)
snapshot_plot(model, device, y=0.5, t=0.0)


