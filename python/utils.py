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



class pitch_encoder:
    """Encodes pitch-type and location to index
    Args:
        ab_array ([type]): [description]
    """
    def __init__(self):

        self.pitch_map = {
            "FF": 1, 
            "SL": 2,
            "FT": 3,   
            "CH": 4,   
            "SI": 5,   
            "CU": 6,  
            "FC": 7,   
            "KC": 8,   
            "FS": 9,   
            "EP": 10,     
            "FO": 11,     
            "PO": 12,     
            "SC": 13,
            "KN": 14
        }
        self.inverse_pitch_map = {v:k for k,v in self.pitch_map.items()}
        self.zones = np.arange(1, 15, 1) # 1-14

    def encode_pitch(self, pitch_type, zone):
        return self.pitch_map[pitch_type] * 14 + int(zone)

    def decode_pitch(self, encoded_pitch):
        pitch_type = self.inverse_pitch_map[np.floor(encoded_pitch/14)]
        zone = encoded_pitch % 14
        return pitch_type, zone