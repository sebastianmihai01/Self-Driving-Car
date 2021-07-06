import torch.nn as nn
import torch.nn.functional as F


class Network(nn.Module):

    hidden_layer1, hidden_layer2, hidden_layer3 = 32, 64, 128

    def __init__(self, input_layer, action):

        super(Network, self).__init__()
        self.input_connection, self.output_connection = None, None
        self.input_layer = input_layer
        self.action = action
        input_connection, output_connection = nn.Linear(self.input_layer, self.hidden_layer),\
            nn.Linear(self.hidden_layer, self.action)

    def ActionSelectionPolicy(self, iterations, state):

        x = F.relu(self.input_connection(state))
        for i in range(1, iterations-1):
            x = F.relu(self.input_connection(state))
        value_selected = self.output_connection(x)

        return value_selected
