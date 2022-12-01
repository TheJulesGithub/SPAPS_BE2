"""
A python word occurence count. This code runs on normal python (no distributions).
"""
from time import time


# Method 1: optimized memory/cpu
# source: https://stackoverflow.com/questions/35857519/efficiently-count-word-frequencies-in-python
start_computing = time()

import io
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

infile = "data/text.txt"

ngram_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1), min_df=1)

with io.open(infile, 'r', encoding='utf8') as fin:
    X = ngram_vectorizer.fit_transform(fin)
    vocab = ngram_vectorizer.get_feature_names()
    counts = X.sum(axis=0).A1
    freq_distribution = Counter(dict(zip(vocab, counts)))
    print(freq_distribution.most_common(10000))

print("Method 1: Time to count words: {} s.".format(time() - start_computing))
