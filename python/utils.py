import numpy as np
import pandas as pd

features = [
    "pitch_type",
    "release_speed",
    "zone",
    "p_throws",
    "stand",
    "type",
    "balls",
    "strikes",
    "outs_when_up",
    "inning",
    "pitch_number",
    "pitch_name",
    "home_score",
    "away_score",
    "if_fielding_alignment",
    "of_fielding_alignment",
    # Add players on base
]


class AtBat:
    """ Class per AB, gives representation in pd.DF and numpy array """

    def __init__(self, dataframe, strikeout_row):
        self.num_pitches = dataframe["pitch_number"].iloc[strikeout_row]
        self.df = dataframe[strikeout_row:strikeout_row+self.num_pitches].iloc[::-1]
        self.np = self.df.to_numpy() # Shape will be (pitches, features)                
