import pandas as pd
import json

slovar = {}
data = pd.read_csv('HLTV_CSGO_results.csv', sep=';')
for i in data.iterrows():
    if i[1][5] < i[1][6]:
        slovar[i[1][2]] = [1, i[1][1], ]
    else:
        slovar[i[1][2]] = [0, i[1][1], ]
data = pd.read_csv('suren.csv')
match_links = []
match_id = []
teamA = []
teamB = []
kefA = []
kefB = []
result = []
for i in data.iterrows():
    match_links.append(slovar[int(i[1][1])][1])
    match_id.append(int(i[1][1]))
    teamA.append(int(i[1][2]))
    teamB.append(int(i[1][3]))
    kefA.append(i[1][4])
    kefB.append(i[1][5])
    result.append(slovar[int(i[1][1])][0])

a = pd.DataFrame({
    'matchLink': match_links,
    'matchId': match_id,
    'teamA': teamA,
    'teamB': teamB,
    'kefA': kefA,
    'kefb': kefB,
    'win': result
})
a.to_csv('suren2.csv')
