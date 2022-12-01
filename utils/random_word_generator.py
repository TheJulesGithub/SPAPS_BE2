"""
This code generate huge text file to get a representative volumetry.

Source: https://www.lipsum.com/feed/html to get 60 paragraph of lorem ipsum (stored into `lorem_ipsum_sample.txt`

Action performed:
* Read `lorem_lipsum_sample.txt`
* Copy it N times
* Write result
Result file shall be a "big data file" of ~1 Go
"""

import os

# Confs
source_file = "lorem_ipsum_sample.txt"

# Number of time file is repeated
N = 30000

# 1/ Read ref
# -----------------------
with open(source_file, "r") as f:
    data = f.read()
    # ex: '\n\nLorem ipsum dolor...'

# 2/ Generate huge file
# -----------------------
data = data * N


# 3/ Write file
# -----------------------
# Go into parent dir
os.chdir('..')
with open("data/text.txt", "w") as f:
    f.write(data)

    print("Process finished with success")
