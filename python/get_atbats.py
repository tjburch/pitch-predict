# Statcast scraper, player lookup
from pybaseball import playerid_lookup, statcast_pitcher

# Numerical tools
import pandas as pd
import numpy as np

# Python tools
import sys

# Local imports
from utils import features, AtBat


def get_atbats(first, last):

    # Lookup player
    player_info = playerid_lookup(last, first)
    player_id = player_info["key_mlbam"].iloc[0]  # assume only one line
    start_year = int(player_info["mlb_played_first"].iloc[0])
    end_year = int(player_info["mlb_played_last"].iloc[0])
    # ignore this year
    if end_year == 2019:
        end_year = 2018

    # Get all the stats
    start_date = "{0}-01-01".format(start_year)
    end_date = "{0}-12-31".format(end_year)
    print("Scraping from {0} to {1}".format(start_date, end_date))
    d_all_stats = statcast_pitcher(start_date, end_date, player_id)
    d_features = d_all_stats[features]

    # Iterate over strikeout rows, build into AtBat Objects
    strikeout_rows = d_all_stats.index[d_all_stats["events"] == "strikeout"].to_list()
    at_bats, ab_arrays = [], []
    for row in strikeout_rows:
        this_ab = AtBat(d_features, row)
        at_bats.append(this_ab)
        ab_arrays.append(this_ab.np)

    return at_bats, ab_arrays


if __name__ == '__main__':
    from seaborn import pairplot
    import matplotlib.pyplot as plt

    # Get info from command line
    first = sys.argv[1]
    last = sys.argv[2]

    ab, arrays = get_atbats(first, last)
    np.save(f"data/{first+last}", arrays)
    # Do some plotting
    dfs = [x.df for x in ab]
    concat_abs = pd.concat(dfs)
    slim_features = [
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
    ]
    concat_abs = concat_abs[slim_features]
    pairplot(concat_abs)

    plt.savefig("vizualizations/{0}_features.png".format(first+last))
