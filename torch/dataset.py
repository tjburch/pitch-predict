""" Create torch dataset for RNN from np feature array
--- WIP: tjb ---
TODO - tests
"""
# Utils
import sys
from collections import Counter

# Math and ML
import numpy as np
import torch

# Local Imports
sys.path.append("../python/")
from feature_array import feature_array

class Dataset(torch.utils.data.Dataset):

    def __init__(self, args, first, last):
        
        # Save Args
        self.args = args

        # Load Feature Array
        self.feature_array = feature_array(first, last)
        self.pitch_strings  = self.feature_array[:,0]
        self.pitch_lists = np.array([x.split() for x in a]).astype(int)

        # Get Unique Pitch Types
        self.arsenal = self.get_unique_pitches()

    def get_unique_pitches(self):
        """ Get unique set of pitches thrown
        -- Similar to a "vocabulary"
        Returns:
            list: List of unique indicies of pitches thrown
        """
        # Get Full Pitch List        
        pitch_list = self.pitch_lists.flatten()
        # Return sorted unique pitch types
        pitch_counts = Counter(pitch_list)
        return sorted(pitch_counts, key=pitch_counts.get, reverse=True)

    # --- Pytorch methods ---
    def __len__(self):
        return len(self.pitch_lists) - self.args.sequence_length
    def __getitem__(self, index):
            return (
                torch.tensor(self.pitch_lists[index:index + self.args.sequence_length]),
                torch.tensor(self.pitch_lists[index+1:index + self.args.sequence_length])
            )