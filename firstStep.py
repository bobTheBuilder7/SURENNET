import pandas as pd
import json

data = pd.read_csv('csgoKefs.csv', sep=';')
match_ids = data['matchLinkId']
teamAID = data['teamAId']
teamBID = data['teamBId']
kefs = []
for i in data['kefs']:
    i = json.loads(i)
    kefs.append(i)
new_kefsA = []
new_kefsB = []
for i in kefs:
    list1 = []
    list2 = []
    for jj in i:
        list1.append(jj[0])
        list2.append(jj[1])
    avg1 = round(sum(list1) / len(list1), ndigits=2)
    avg2 = round(sum(list2) / len(list2), ndigits=2)
    new_kefsA.append(avg1)
    new_kefsB.append(avg2)
a = pd.DataFrame({
    'matchLinkId': match_ids,
    'teamAId': teamAID,
    'teamBId': teamBID,
    'kefsA': new_kefsA,
    'kefsb': new_kefsB
})
a.to_csv('suren.csv')