import torch.nn as nn
import torch.optim as optim
import torch
from Residuals import burgers_equation_residual, initial_boundary_loss
from Data import get_data

class BurgersNet(nn.Module):
    def __init__(self, hidden_layers=8, neurons=20):
        super(BurgersNet, self).__init__()
        layers = [nn.Linear(2, neurons), nn.Tanh()]
        for _ in range(hidden_layers):
            layers += [nn.Linear(neurons, neurons), nn.Tanh()]
        layers += [nn.Linear(neurons, 1)]
        self.model = nn.Sequential(*layers)

        self.train_errors = []
        self.test_errors = []

    def forward(self, t, x):
        input = torch.cat([t, x], dim=1)
        return self.model(input)

    def fit(self, device, epochs):
        opt = optim.Adam(self.parameters(), lr=5e-4)

        train_data, test_data = get_data(device)
        x_d, t_d, x_c, t_c, u_d = train_data[0], train_data[1], train_data[2], train_data[3], train_data[4]
        x_d_test, t_d_test, x_c_test, t_c_test, u_d_test = test_data[0], test_data[1], test_data[2], test_data[3], test_data[4]

        for epoch in range(epochs):
            opt.zero_grad()
            train_loss = burgers_equation_residual(self, t_c, x_c) + initial_boundary_loss(self, u_d, t_d, x_d)
            test_loss = burgers_equation_residual(self, t_c_test, x_c_test) + initial_boundary_loss(self, u_d_test, t_d_test, x_d_test)
            train_loss.backward()
            opt.step()
            self.train_errors.append(train_loss.item())
            self.test_errors.append(test_loss.item())
            if (epoch + 1) % 1000 == 0 or epoch == 0:
                print(f"Epoch {0 if epoch == 0 else epoch + 1}, Train-Loss: {train_loss.item():.6f}, Test-Loss: {test_loss.item():.6f}")

        return self.train_errors, self.test_errors