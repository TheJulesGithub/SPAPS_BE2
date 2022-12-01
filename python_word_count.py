"""
A python word occurence count. This code runs on normal python (no distributions).
"""
from time import time
from collections import Counter

start_computing = time()

# 1/ Read file
with open("SPAPS_BE2/data/text.txt") as f:
    data = f.read()

# 2/ Count words
# Split by lines (if split by " ", memory error)
d = data.split("\n\n")


# Result dict (in fact `counter` object) to fill
result = Counter({})
for k in d:  # read each line of the file and count words
    current_result = Counter(k.split(" "))
    result = result + current_result

# Display results
print(result)

print("Pyspark method: Time to count words: {} s.".format(time() - start_computing))

