import json

data = []
with open("tttt/data.json", "r", encoding='utf-8-sig') as f:
    data.append(json.load(f))
with open("tttt2/data.json", "r", encoding='utf-8-sig') as f:
    data.append(json.load(f))
# print(data1)
# print(data2)

for city, dists in data[0].items():
    for dist in dists.keys():
        if set(data[0][city][dist]) != set(data[1][city][dist]):
            print(city, dist)
            if not (diff := list(set(data[0][city][dist]) - set(data[1][city][dist]))):
                print(list(set(data[1][city][dist]) - set(data[0][city][dist])))
            else:
                print(diff)
