# -*- coding: cp950 -*-
# -*- coding: utf-8 -*-
import pymysql
from pathlib import Path
from shutil import rmtree
import pandas


def executeScriptsFromFile(filename):
    with open(str(Path.cwd()) + '/' + filename, 'r', encoding="utf-8") as fd:
        sql_file = fd.read()
    commands = sql_file.split(';')
    commands.pop()
    for command in commands:
        try:
            cursor.execute(command)
        except Exception as error_message:
            print("Command skipped: ", error_message)


def dropTable(table_name):
    try:
        cursor.execute(f'drop table if exists {table_name};')
    except Exception as error_message:
        print("Command skipped: ", error_message)


conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='00000000',
    db='puppy',
    charset='utf8mb4',
)
cursor = conn.cursor()

dropTable("timingLocation")
dropTable("join_plan")
dropTable("user")
dropTable("data")

for path in Path.cwd().parent.iterdir():
    if path.match('*計畫*'):
        print('del', path)
        rmtree(path, ignore_errors=True)

executeScriptsFromFile('create_table.sql')
conn.commit()

df = pandas.read_excel("1090822訪員名單.xlsx")
# print(df)
# df = pandas.read_excel("學生帳密.xlsx")
# count = len(list(df['姓名']))
data = [list(df['App帳號']),list(df['App密碼']),list(df['姓名'])]
for i in range(len(data[0])):
    cursor.execute('insert into user value (%s,%s,%s)', (data[0][i], data[1][i], data[2][i]))
    conn.commit()
conn.close()
