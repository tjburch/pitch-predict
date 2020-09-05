
from get_atbats import get_atbats
from utils import pitch_encoder


def generate_data(first, last):
    
    # Get all AB micro-dataframes
    at_bats = get_atbats(first, last)

    n_features = 5 # TODO
    output_array = np.zeros(len(at_bats),n_features)

    # Add sequential Data
    for i, ab in enumerate(at_bats):
        # Get rec_array
        at_bat_records = at_bats.rec_array

        # Set as row in dataframe
        pitch_types = at_bat_records["pitch_type"]
        pitch_zones = at_bat_records["zone"]
        
        pitches = []
        for t, z in zip(pitch_types, pitch_zones):
            # TODO: consider parallelization
            pitches.append(pitch_encoder(pitch_type=t, pitch_zone=z))
        
        output_array[i,0] = " ".join(pitches)

        # Add state data
        # -- ASSUMPTION -- state data is the same for all pitches
        output_array[i,1] = at_bat_records["stand"][0]
        output_array[i,2] = at_bat_records["outs_when_up"][0]
        output_array[i,3] = at_bat_records["inning"][0]
        # Pitch number -> Pitches at start of AB
        output_array[i,4] = at_bat_records["pitch_number"][0]
        # Scoree differential
        if home_team: # TODO - figure out how to set this
            output_array[i,5] = at_bat_records["home_score"][0] - at_bat_records["away_score"][0]
        else: # TODO - figure out how to set this
            output_array[i,5] = at_bat_records["away_score"][0] - at_bat_records["home_score"][0]



    

