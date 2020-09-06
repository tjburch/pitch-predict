
import numpy as np
from get_atbats import get_atbats
from utils import pitch_encoder, features

def feature_array(first, last):
    
    # Get all AB micro-dataframes
    at_bats = get_atbats(first, last)

    n_features = len(features) - 1 # subtract 1 for fld/bat score becoming differential

    # Add sequential Data
    array_builder = []
    for i, ab in enumerate(at_bat_records):

        # Set as row in dataframe
        quantities = []
        pitch_types = ab["pitch_type"]
        pitch_zones = ab["zone"]
        
        pitches = []
        for t, z in zip(pitch_types, pitch_zones):
            
            pitches.append(pitch_encoder(pitch_type=t, pitch_zone=z))
            

        if len(pitches) == 1:
            quantities.append(str(pitches[0]))
        else:
            quantities.append(" ".join([str(p) for p in pitches]))

        # Add state data
        # -- ASSUMPTION -- state data is the same for all pitches
        quantities.append(ab["stand"][0])
        quantities.append(ab["outs_when_up"][0])
        quantities.append(ab["inning"][0])
        # Pitch number -> Pitches at start of AB
        quantities.append(ab["pitch_number"][0])
        # Score differential
        quantities.append(ab["fld_score"][0] - ab["bat_score"][0])

        # Base occupancy
        # - NANs for unoccupied, so invert isnan bool
        # Could afford to make this more robust against steals.
        quantities.append(np.invert(np.isnan(ab["on_1b"][0])))
        quantities.append(np.invert(np.isnan(ab["on_2b"][0])))
        quantities.append(np.invert(np.isnan(ab["on_3b"][0])))

        array_builder.append(quantities)
    
    output_array = np.array(array_builder)

