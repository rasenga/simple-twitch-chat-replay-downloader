import requests
import json
import sys
import csv
import pandas as pd
import re
import string
from itertools import chain
frequency = {}


data = pd.read_csv("687103734.csv")
tmp_data = data
time_list = tmp_data.drop_duplicates("time", keep="first")[
    'time'].values.tolist()
for i in time_list:
    chat = "".join(list(chain(*data[data['time'].isin([i])].drop(
        'time', axis=1).values.tolist()))).lower()
    print(chat)
    match_pattern = re.findall(r'[ㅋ]', chat)
    print(len(match_pattern))
    # for word in match_pattern:
    #     count = frequency.get(word, 0)
    #     frequency[word] = count + 1

    # frequency_list = frequency.keys()

    # for words in frequency_list:
    #     print words, frequency[words]
