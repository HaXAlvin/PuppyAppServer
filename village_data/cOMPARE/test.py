import pandas
import json
df = pandas.read_excel("1090720遊蕩犬調查區完整版.xlsx")
with open('data.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
count = 0
for i in df[['縣市','鄉鎮市區','村里']].values:
    for j in range(3):
        i[j] = i[j].replace("台","臺")
    if i[1] not in data[i[0]]:
        print(count+2,i[0],i[1],i[2])
    elif not i[2] in data[i[0]][i[1]]:
        print(count+2,i[0],i[1],i[2])
    count+=1