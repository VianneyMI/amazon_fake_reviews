import pandas as pd
import numpy as np

data = pd.read_csv('amazon_reviews.txt', delimiter="\t")
print(data.head())

# %% Average length of words in a review
review_text = data.iloc[0, 8]
print('example review:', review_text)

word_len = list(map(len, review_text.split()))  # length of each word in sentence
print('average word length: ', np.mean(word_len))
