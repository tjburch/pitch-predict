"""
LSTM PyTorch Model
--- WIP: tjb ----
Modeling off of: https://www.kdnuggets.com/2020/07/pytorch-lstm-text-generation-tutorial.html
"""
import torch
from torch import nn

class Pitch_lstm(nn.Module):
    """ ad hoc prototyping model to start with """
    def __init__(self, dataset):
        super(Model, self).__init__()
        self.lstm_size = 128
        self.embedding_dim = 128
        self.num_layers = 3

        # Get number of unique pitches
        # - Think "vocabulary" for text
        # - Value is number of unique pitches thrown * number of locaitons (14 likely)
        n_unique_pitches = set() # TODO: Fill in pitches from dataset

        self.embedding = nn.Embedding(
            num_embeddings = n_unique_pitches,
            embedding_dim = self.embedding_dim
        )
        self.lstm = nn.LSTM(
            # input_size - expected features in input 
            input_size=self.lstm_size,
            # hidden_size - features in hidden state
            hidden_size=self.lstm_size, # TODO: maybe more flexible
            # num_layers - number of recurrent layers
            num_layers=self.num_layers,
            # Standard regularization dropout
            dropout=0.2
        )
        self.fc = nn.Linear(self.lstm_size, )

    def forward(self, x, prev_state):

        embed = self.embedding(x)
        output, state = self.lstm(embed, prev_state)
        logits = self.fc(output)
        return logits, state

    def init_state(self, sequence_length):
        return (
            torch.zeros(self.num_layers, sequence_length, self.lstm_size),
            torch.zeros(self.num_layers, sequence_length, self.lstm_size)
        )