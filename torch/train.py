
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
from model import Pitch_lstm
from dataset import Dataset
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e","--max-epochs", type=int, default=10)
parser.add_argument("-b","--batch-size", type=int, default=256)
parser.add_argument("-s","--sequence-length", type=int, default=4)
args = parser.parse_args()

def train(dataset, model, args):
    # Put torch model in training mode
    model.train()
    
    # Setup Dataloader, loss function, optimizer
    dataloader = DataLoader(dataset, batch_size=args.batch_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(args.max_epochs):
        state_h, state_c = model.init_state(args.sequence_length)

        for batch, (x,y) in enumerate(dataloader):
            optimizer.zero_grad()

            y_pred, (state_h, state_c) = model(x, (state_h, state_c))
            loss = criterion(y_pred.transpose(1, 2), y)

            state_h = state_h.detach()
            state_c = state_c.detach()

            ## learning
            loss.backward()
            optimizer.step()

            print({
                'epoch': epoch,
                'batch': batch,
                'loss': loss.item()
            })


def predict(dataset, model, pitches, n_to_predict=1):
    """Prediction Routine
    Args:
        dataset (torch.Dataloader): Filled dataloader
        model (torch.NN): Trained pytorch NN
        pitches (list): Previous pitches seen in AB
        n_to_predict (int, optional): Number of pitches to predict. Defaults to 1.

    Returns:
        [type]: [description]
    """
    model.eval()

    # Initalize model
    state_h, state_c = model.init_state(len(pitches))

    for i in range(0, next_seq_len):
        # Set x to pitch list so far
        x = torch.tensor(pitches)
        # Get prediction probability 
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))
        last_pitch_logits = y_pred[0][-1]
        p = torch.nn.functional.softmax(last_pitch_logits, dim=0).detach().numpy()
        # Randomly select pitch according to assigned probability
        pitch_chosen = np.random.choice(len(last_pitch_logits), p=p)
        # Append selected pitches
        pitches.append(pitch_chosen)

    return pitches



if __name__ == "__main__":
    """Main routine to train and save model
    """
    pitcher_data = Dataset("austin","gomber", args)
    model = Pitch_lstm(pitcher_data)
    train(pitcher_data, model, args)
    torch.save(model.state_dict(),"test_model")