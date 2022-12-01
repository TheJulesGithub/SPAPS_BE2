"""
This code permits to generate a "big data" file of ~1Go containing (fake) telemetry data.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 1/ Confs
# -----------------------------------------
SEED=1
np.random.seed(SEED)
N_TM = 500  # Number of Telemetry to generate
N_DAYS = 10  # Number of days to generate
NB_HOLES = 5  # Number of holes to generate
NB_SPIKES = 1  # Number of spike to generate in TM_1
SPIKES_VALUES = 10e4  # Value taken by spike

# 1/ Create df
# -----------------------------------------
end_time = datetime.today()
# ex: '11/16/2022, 17:34:05'

# X days before
start_time = end_time - timedelta(days=N_DAYS)

n_points = N_DAYS * 24 * 60 * 60 # Seconds in `N_DAYS` days

df_time = pd.date_range(start=start_time,
                        end=end_time,
                        periods=n_points)
# ex:Series(['2021-03-25 14:22:24.824136', ...])

# Into df
df_time = pd.Series(df_time).to_frame("time")

# Add timestamp col
df_time['datetime'] = df_time[['time']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)


# Add `is_hole` col permitting to create holes
df_time["is_hole"] = 0
df_time.set_index("time", inplace=True)

# Add a `orbit_id` col
# One orbit = n_points / n_orbits
nb_orbits = N_DAYS  # 1 orbit = 1 day

orbits = [[k] * (round(len(df_time)/10)) for k in range(nb_orbits)]

# flatten
flat_orbit_list = [item for sublist in orbits for item in sublist]

df_time['orbit_id'] = flat_orbit_list

# Sort
df_time.sort_index(inplace=True)

# Artificially create holes
# 
# Create `nb_holes`:
# * at random location (`hole_list`)
# * with random legth (`hole_duration`) -> get some holes with large duration
# 
# Note: usage of a seed at the beginning of the script to get reproducible results.

# Index of first points of the hole to create
hole_list = np.random.choice(range(len(df_time)), NB_HOLES, replace=False)

# duration of each holes (in nb of points)
hole_duration = np.random.randint(low=10,
                                  high=n_points * 0.10,  # 10% of the nb points
                                  size=NB_HOLES)

# Update col "is hole"
df_with_holes = df_time.copy(deep=True)

for i, hole_index in enumerate(hole_list):
    
    current_hole_duration = hole_duration[i]  # ex: 25, means 25 next pts shall be rm
    
    # Update col "is_hole"
    df_with_holes.loc[hole_index:(hole_index + current_hole_duration), 'is_hole']=1
    # ex: ['2021-03-25 14:31:39.412124843',...]

# Final format
series_data = df_with_holes[df_with_holes['is_hole'] != 1].index.to_series().sort_values()

# Create data

# Drop holes
df = df_with_holes[df_with_holes['is_hole'] != 1]

df.drop(columns='is_hole', inplace=True)


# Create fake cols of values
# for k in range(N_TM):
df[["tm_{}".format(k) for k in range(N_TM)]] = np.random.randint(0, 10, size=(len(df), N_TM))

df = df.reset_index()


# Create shifts (one for TM 2)
# 
# * Choose one orbit
# * plus 200%

orbit_to_shift = 2


# 200% shift 
new_value = df[df.orbit_id == orbit_to_shift]['tm_2'] * 2
df.loc[df.orbit_id == 2, 'tm_2'] = new_value

# Artificially create spikes : one per TM
# 
# At random loc

for tm_id in range(N_TM):

    # Tm name
    tm = 'tm_{}'.format(tm_id)

    # Determine (randomly) if first TM shall have consecutive spikes or not
    is_consecutive = np.random.choice([True, False])

    # If consecutive:...
    if is_consecutive:
        # Generate the position of the first oultier (the second one shall be at position+1)
        spike_index = np.random.randint(0, len(df) -1)
        
        spike_position = df.iloc[[spike_index, spike_index+1]].index.values
        
        df.loc[spike_position, tm] = SPIKES_VALUES

    else:
        # Generate just one spike
        spike_index = np.random.randint(0, len(df) -1)
        
        spike_position = df.iloc[[spike_index]].index.values
        
        df.loc[spike_position, tm] = SPIKES_VALUES

    # Next TM=> generate the contrary situation
    is_consecutive = not is_consecutive


# Write result in a csv
# Go into parent dir
os.chdir("..")
df.to_csv("data/data.csv", index=False)
