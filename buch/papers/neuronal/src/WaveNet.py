import torch.nn as nn
import torch.optim as optim
from Residuals import total_loss

class WaveNet(nn.Module):
    train_error = []
    test_error = []

    def __init__(self):
        super(WaveNet, self).__init__()
        self.net = nn.Sequential(
            # Input layer with 3 input units for x, y and t
            nn.Linear(3, 5),
            nn.Tanh(),
            # First hidden layer
            nn.Linear(5, 5),
            nn.Tanh(),
            # Output layer with a single output unit for the z-coordinate
            nn.Linear(5, 1)  # Output u(x, y, t)
        )

    def forward(self, x):
        return self.net(x)

    # Train model
    def fit(self, x_train, y_train, t_train, x_test, y_test, t_test, device, n_epochs):
        optimizer = optim.Adam(self.parameters(), lr=0.001)
        for epoch in range(n_epochs):
            optimizer.zero_grad()

            train_loss = total_loss(self, x_train, y_train, t_train, device)
            test_loss = total_loss(self, x_test, y_test, t_test, device)

            train_loss.backward()
            optimizer.step()

            self.train_error.append(train_loss.item())
            self.test_error.append(test_loss.item())

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Train-Loss: {train_loss.item():.6f}, Test-Loss: {test_loss.item():.6f}")

        return self.train_error, self.test_error
