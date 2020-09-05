import numpy as np
import pandas as pd

features = [
    "pitch_type",
    "zone",
    "stand",
    "outs_when_up",
    "inning",
    "pitch_number",
    "home_score",
    "away_score", # Change these to run diff
    "if_fielding_alignment",
    "of_fielding_alignment",
    # Add players on base
]


class AtBat:
    """ Class per AB, gives representation in pd.DF and numpy array """

    def __init__(self, dataframe, strikeout_row):
        self.num_pitches = dataframe["pitch_number"].iloc[strikeout_row]
        self.df = dataframe[strikeout_row:strikeout_row+self.num_pitches].iloc[::-1]
        self.np = self.df.to_numpy() # Raw numpy array
        self.rec_array = self.df.to_records() # rec_array


def pitch_encoder(pitch_type=None, pitch_zone=None, encode=True):
    """Encodes pitch-type and location to index
    (this could be two functions, but wanted to keep the maps in one place)
    Args:
        encode (bool): Encode or decode pitch 
    """
    if (encode and pitch_type == None) or (encode and pitch_zone == None):
        raise ValueError("If encoding, need to patch pitch type and zone")

    pitch_map = {
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
    zones = np.arange(1, 15, 1) # 1-14

    # Decide if encoding or decoding
    if encode:
        # Return Index
        return (pitch_map[pitch_type] * 14 + int(pitch_zone))
    else:
        # Get and return type and zone
        inverse_pitch_map = {v:k for k,v in self.pitch_map.items()}
        pitch_type = inverse_pitch_map[np.floor(encoded_pitch/14)]
        pitch_zone = encoded_pitch % 14
        return pitch_type, pitch_zone