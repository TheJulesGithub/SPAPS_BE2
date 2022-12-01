""""
This script permits to run a Pyspark word count script.
"""

# To create a SparkSession:
from pyspark.sql import SparkSession
from time import time

start_computing = time()

# Create spark session
spark_session = SparkSession.builder.getOrCreate()

# Read a text file lines by lines
lines=spark_session.sparkContext.textFile('text.txt')
# ex: [' 01 ', '03/22 08:51:01 INFO   :.main: *************** RSVP Agent started ***************', ...]
# Faltten (1 word by 'line')
words = lines.flatMap(lambda line: line.split(' '))
# ex: ['', '01', '', '03/22',...]

# Create a "key- value pairing" (key=word, value=1)
words_with_1 = words.map(lambda word: (word, 1))
# ex: [[('', 1), ('01', 1), ('', 1), ('03/22', 1),...]

# Sum all "values" having the same "keys" (same word)
word_counts = words_with_1.reduceByKey(lambda count1, count2: count1 + count2)
# Ex: [('', 104), ('03/22', 52), ...]

# Launch process and retrieve result (ACION)
result = word_counts.collect()

# Display results
print(result)

print("Pyspark method: Time to count words: {} s.".format(time() - start_computing))