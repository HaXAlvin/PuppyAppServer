import pandas as pd
import json

df = pd.read_excel('data.xlsx', encoding='UTF-8').to_numpy()
newdict = {}
for i in df:
    i[0] = str(i[0]).replace("台", "臺")
    i[1] = str(i[1]).replace("台", "臺")
    i[2] = str(i[2]).replace("台", "臺")
    if i[0] not in newdict:
        newdict[i[0]] = {i[1]: [i[2]]}
        continue
    if i[1] not in newdict[i[0]]:
        newdict[i[0]][i[1]] = [i[2]]
        continue
    newdict[i[0]][i[1]].append(i[2])
# newdict=sorted(newdict)
# for city,dist in newdict.items():
#     for dist,villlist in dist.items():
#         villlist.sort()
with open('data.json', 'w', encoding='utf-8-sig') as f:
    # json.dump(newdict, f)
    f.write(json.dumps(newdict, ensure_ascii=False))
# switch(city){
#     case '台北市':
#         switch(distinct){
#             case '松山區':
#                 village = [里];
#                 break;
#             case ''
#         }
#         break;
# }
# with open('data.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# large = "switch(city){{a}}"
# large_case = "case '{a}':{c}{b} break; "
# dist = "distinctList={a}"
# mid = "switch(distinct){{a}}"
# mid_case = "case '{a}':villageList={b} break;"
# villages = []
#
# allLC = ""
# for key, value in data.items():  # key=縣市 val=區{}
#     newDIST = dist
#     newDIST = newDIST.replace("{a}", "['" + ("','".join(value.keys())) + "'];")
#     print(newDIST)
#     newLC = large_case
#     allMC = ""
#     for skey, svalue in value.items():
#         # print(skey,svalue)
#         newMC = mid_case
#         newMC = newMC.replace('{a}', skey)
#         newMC = newMC.replace('{b}', "['" + ("','".join(svalue)) + "'];")
#         # newMC.format("'"+skey+"'", ",".join(svalue))
#         allMC += newMC
#     newM = mid
#     newM = newM.replace("{a}", allMC)
#
#     newLC = newLC.replace("{a}", key)
#     newLC = newLC.replace("{b}", newM)
#     newLC = newLC.replace("{c}", newDIST)
#     # newLC.format(key,newM)
#     allLC += newLC
# # print(allLC)
# large = large.replace("{a}", allLC)
# # print(large)
# with open('for.txt', 'w', encoding='utf-8') as f:
#     f.write(large)
