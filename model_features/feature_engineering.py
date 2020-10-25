# %%
import os
import pyodbc
import pandas as pd
import numpy as np
import nltk  # use for feature engineering
from wordcloud import WordCloud, STOPWORDS  # quick plot of words in the data
import matplotlib.pyplot as plt


# %% Load the amazon reviews
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=..\\data\\exports\\test_appliances.accdb')
cursor = conn.cursor()
sql = "select * from Test_appliances"
data = pd.read_sql(sql, conn)
print(data.head())

# %% See popular words in review title and review
stopwords = set(STOPWORDS)  # remove very frequent words with little meaning (Example: "We", "are" and "the" )
separator = ' '

'''Set plot for review titles and reviews'''
df_cols = ["summary", "reviewText"]
plt.figure()
for i, col in enumerate(df_cols):
    joined_text = separator.join(data[col])
    wc = WordCloud()  # initialize wordcloud object
    wc.generate(joined_text)  # generate wordcloud plot
    plt.subplot(1, 2, i + 1)
    plt.imshow(wc, interpolation='bilinear')  # show plot (interpolation makes the image smooth)
    plt.title(f"Common Words: {col}", fontsize=18)
    plt.axis("off")


# %% Average length of words in a review
data['avg_word_length'] = [None] * len(data)  # preallocate array

for index, row in data.iterrows():
    word_len = list(map(len, row['reviewText'].split()))  # list of lengths of each word in review
    data.loc[index, 'avg_word_length'] = np.mean(word_len)

plt.figure()
plt.hist(data['avg_word_length'], bins=100, log=True)
plt.xlabel('Average word length in review', fontsize=16)
plt.ylabel('Frequency', fontsize=16)
plt.grid()
plt.show()

# %% Repeated reviews

