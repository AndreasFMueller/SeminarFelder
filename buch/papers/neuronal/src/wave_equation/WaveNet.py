import torch.nn as nn
import torch.optim as optim
import torch
import boundaries
from Residuals import total_loss, wave_equation_residual, boundary_condition_loss, initial_condition_loss

class WaveNet(nn.Module):
    train_error = []
    test_error = []

    def __init__(self):
        super(WaveNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 128)
        self.fc4 = nn.Linear(128, 1)
        self.act = nn.Tanh()

        self.init_weights()

    def init_weights(self):
        with torch.no_grad():
            # Glorot Normal
            self.fc1.weight.normal_(0, 2 / (self.fc1.in_features + self.fc1.out_features))
            self.fc1.bias.normal_(0, 2 / (self.fc1.in_features + self.fc1.out_features))

            self.fc2.weight.normal_(0, 2 / (self.fc2.in_features + self.fc2.out_features))
            self.fc2.bias.normal_(0, 2 / (self.fc2.in_features + self.fc2.out_features))

            self.fc3.weight.normal_(0, 2 / (self.fc3.in_features + self.fc3.out_features))
            self.fc3.bias.normal_(0, 2 / (self.fc3.in_features + self.fc3.out_features))

            self.fc4.weight.normal_(0, 2 / (self.fc4.in_features + self.fc4.out_features))
            self.fc4.bias.normal_(0, 2 / (self.fc4.in_features + self.fc4.out_features))

    def forward(self, xyt):
        x = xyt[:, 0:1]
        y = xyt[:, 1:2]
        t = xyt[:, 2:3]

        xy = torch.sin(torch.pi * x) * torch.sin(torch.pi * y)
        xyt = torch.cat([xy, x, y, t], dim=-1)

        xyt = self.act(self.fc1(xyt))
        xyt = self.act(self.fc2(xyt))
        xyt = self.act(self.fc3(xyt)) # (torch.pi / 1.062)
        xyt = self.fc4(xyt)
        return xyt

    # Train model
    def fit(self, x_train, y_train, t_train, x_test, y_test, t_test, device, n_epochs):
        optimizerAdam = optim.Adam(self.parameters(), lr=0.001)
        self.train()

        for epoch in range(n_epochs):
            optimizerAdam.zero_grad()

            train_loss = total_loss(self, x_train, y_train, t_train, device)
            test_loss = total_loss(self, x_test, y_test, t_test, device)
            train_loss.backward()
            optimizerAdam.step()

            self.train_error.append(train_loss.item())
            self.test_error.append(test_loss.item())

            if (epoch + 1) % 100 == 0 or epoch == 0:
                print(f"Epoch {0 if epoch == 0 else epoch + 1}, Train-Loss: {train_loss.item():.6f}, Test-Loss: {test_loss.item():.6f}")
            if epoch + 1 == n_epochs:
                wave_residual = wave_equation_residual(self, x_train, y_train, t_train, device)
                boundary_residual = boundary_condition_loss(self, x_train, y_train, t_train, device, lambd=1)
                initial_residual = initial_condition_loss(self, x_train, y_train, device, lambd=1)
                print("\nUnweighed final loss: " + str(torch.mean(wave_residual + boundary_residual + initial_residual))+"\n")

        return self.train_error, self.test_error

