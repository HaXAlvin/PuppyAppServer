import pandas
from json import dump
json = {}
for j in range(0, 22):
    df = pandas.read_csv(f"./villmast_excel ({j}).csv")
    for i in df[["市縣別", "鄉鎮市", "村里別"]].values:
        i[0] = str(i[0]).replace("台", "臺")
        i[1] = str(i[1]).replace("台", "臺")
        i[2] = str(i[2]).replace("台", "臺")
        if i[0] not in json.keys():
            json[i[0]] = {i[1]: [i[2]]}
        elif i[1] not in json[i[0]].keys():
            json[i[0]][i[1]] = [i[2]]
        else:
            json[i[0]][i[1]].append(i[2])
# json = sorted(json)
# for city,dist in json.items():
#     for dist,villlist in dist.items():
#         villlist.sort()
with open("data.json", "w", encoding="utf-8-sig") as write_file:
    dump(json, write_file, ensure_ascii=False, indent=4)
