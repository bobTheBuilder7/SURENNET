import pandas as pd
import json

urls_new = []
data = pd.read_csv('cs_hltv_data.csv')
for i in data.iterrows():
    # print(i[1][5])
    # print(i[1][6])
    urls_new.append(i[1]['url'])
urls_suren = []
data = pd.read_csv('bot_true/suren2.csv')
for i in data.iterrows():
    urls_suren.append(i[1][1])
k = 0
for i in urls_new:
    if i not in urls_suren:
        k += 1

print(k)
