from flask import Flask, request, jsonify
import requests
import base64
from pathlib import Path
import pymysql
from DBUtils.PooledDB import PooledDB
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask_apscheduler import APScheduler
from time import sleep, gmtime, strftime
# need to change path password host
app = Flask(__name__)
scheduler = APScheduler()
POOL = PooledDB(
    creator=pymysql,  # 使用連結資料庫的模組
    maxconnections=10,  # 連線池允許的最大連線數，0和None表示不限制連線數
    mincached=5,  # 初始化時，連結池中至少建立的空閒的連結，0表示不建立
    maxcached=0,  # 連結池中最多閒置的連結，0和None不限制
    blocking=True,  # 連線池中如果沒有可用連線後，是否阻塞等待。True，等待；False，不等待然後報錯
    maxusage=None,  # 一個連結最多被重複使用的次數，None表示無限制
    setsession=[],  # 開始會話前執行的命令列表。如：["set dateStyle to ...", "set time zone ..."]
    ping=2,
    # ping MySQL服務端，檢查是否服務可用。
    # 0 = never, 1 = default = whenever it is requested
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='127.0.0.1',
    port=3306,
    user='root',
    password='00000000',
    # password='0000',
    database='puppy',
    charset='utf8mb4',
    read_timeout=10,
    autocommit=True
)


class Config(object):
    SCHEDULER_API_ENABLED = True,


@scheduler.task('interval', id='LocationAPS', seconds=600, misfire_grace_time=900)
def insert_timingLocation():
    print(f"Location Start Insert At {strftime('%H:%M:%S', gmtime())}")
    conn = POOL.connection()
    try:
        with conn.cursor() as cursor:
            while LocationArray:
                try:
                    sql = "insert into timingLocation value (%s,%s,%s,%s,%s)"
                    cursor.execute(sql, LocationArray[0])
                except pymysql.err.Error as err:
                    print(err)
                print(f"clear {LocationArray[0]} left {len(LocationArray) - 1}")
                LocationArray.pop(0)
                sleep(1)
    except pymysql.err.Error as err:
        print(err)
    finally:
        conn.close()
    print(f"Location End Insert At {strftime('%H:%M:%S', gmtime())}")
    return


def get_data(req):
    if not req.is_json:
        return False, jsonify({"success": False, "msg": "Not Json"})
    data = req.get_json()
    print([j for i, j in data.items() if i != "img"])
    if "" in data.values():
        return False, jsonify({"success": False, "msg": "Empty Columns"})
    return True, data


def get_max_id(plan, user):
    conn = POOL.connection()
    try:
        with conn.cursor() as cursor:
            sql = "select max(id) from data where plan=%s and user=%s"
            val = (plan, user)
            cursor.execute(sql, val)
            max_id = cursor.fetchone()[0]
            if not max_id:
                max_id = 0
            return int(max_id)  # id = 流水號
    except pymysql.err.Error as err:
        print(err)
        return None
    finally:
        conn.close()


def is_user_exist(plan, user):
    conn = POOL.connection()
    try:
        with conn.cursor() as cursor:
            sql = "select * from user where plan=%s and user=%s"
            val = (plan, user)
            if True in [not i for i in val]:
                return {"success": False, "msg": "Empty Column"}
            # if False in [i.isdigit() for i in val]:
            #     return {"success": False, "msg": "Not Allowed Word"}
            cursor.execute(sql, val)
            res = cursor.fetchall()
            print(res)
            if not res:
                return {"success": False, "msg": "not exist"}
    except pymysql.err.Error as err:
        print(err)
        return {"success": False, "msg": "user sql error"}
    finally:
        conn.close()
    return {"success": True, "id": 0, "name": res[0][2]}


@app.route('/')
def index():
    return 'are you kidding?'


@app.route('/timingLocation', methods=['POST'])
def timingLocation():
    success, data = get_data(request)
    if not success:
        return data
    LocationArray.append(list(data.values()))
    return jsonify({"success": True})


@app.route('/authUser', methods=['POST'])
def authUser():
    success, data = get_data(request)
    if not success:
        return data
    res = dict(is_user_exist(data['plan'], data['user']))
    if not res['success']:
        return jsonify(res)
    if max_id := get_max_id(data['plan'], data['user']):
        res['id'] = max_id
    print("return max id :", max_id)
    return jsonify(res)


@app.route('/authLocation', methods=['POST'])
def authLocation():
    success, data = get_data(request)
    if not success:
        print("auth error")
        return data
    params = {'format': 'json', 'lat': data['lat'], 'lon': data['lon']}
    # url = 'http://140.134.79.128:8888/nominatim/reverse'
    url = 'http://140.116.152.77:40130/nominatim/reverse'
    result = requests.post(url, params=params).json()
    if (msg := result.get('error')) is not None:
        print(msg)
        return jsonify({'success': False, 'msg': msg})
    try:
        address = result['address']
        print(address)
        resp = {
            'success': True,
            'suburb': address.get('suburb') if address.get('suburb') else address.get('town'),
            'city_district': address.get('city_district'),
            'city': address.get('city') if address.get('city') else address.get('county')
        }
        resp['city'] = resp['city'].replace('台', '臺')

    except KeyError:
        print("auth key error")
        return jsonify({'success': False, 'msg': result['address']})
    if None in resp.values():
        print("auth none error")
        return jsonify({'success': False, 'msg': result['address']})
    return jsonify(resp)


@app.route('/img_upload', methods=['POST'])
def img_upload():
    print(request.headers)

    success, data = get_data(request)
    if not success:
        print(data)
        return data
    # path
    path = Path(f"計畫{data['plan'].zfill(2)}/{data['city']}/{data['district']}/{data['village']}")
    # path = Path(f"H:/計畫{data['plan'].zfill(2)}/{data['city']}/{data['district']}/{data['village']}")
    exist = is_user_exist(data['plan'], data['user'])
    if not exist['success']:
        return jsonify(exist)

    max_id = get_max_id(data['plan'], data['user'])
    if max_id is None:
        return jsonify({'success': False, 'msg': 'max_id sql error'})

    conn = POOL.connection()
    try:
        with conn.cursor() as cursor:
            # check already exist img
            sql = "select * from data where id=%s and plan=%s and user=%s"
            val = (data['id'], data['plan'], data['user'])
            cursor.execute(sql, val)
            finds = cursor.fetchall()
            if finds:
                return jsonify({'success': False, 'msg': 'Same PK', 'id': max_id})
        with conn.cursor() as cursor:
            # add img to mysql
            sql = "insert into data value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            val = list(data.values())
            val[3] = str(path)
            val.pop(-1)  # del "update_data":true
            cursor.execute(sql, val)

    except pymysql.err.Error as err:
        print(err)
        return jsonify({'success': False, 'msg': f'img upload sql error :{err}'})
    finally:
        conn.close()

    Path.mkdir(path, parents=True, exist_ok=True)
    # file name
    # data["user"] = data["user"].zfill(3)
    data["dayCount"] = data["dayCount"].zfill(2)
    count = str(int(max_id) + 1).zfill(3)
    location = f'{data["city"]}{data["district"]}{data["village"]}'
    fileName = f'訪員{exist["name"]}-{location}第{data["dayCount"]}天第{count}張.png'
    # origin img
    img = Image.open(BytesIO(base64.b64decode(data['img']))).convert("RGBA")
    # txt img
    txtImg = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txtImg)
    txt = f'{data["date"][:10]}\n{location}\n{str(data["lat"])[:8]},{str(data["lon"])[:7]}'
    draw.text((0, 0), txt, (139, 69, 19, int(0.8 * 255)), font=ImageFont.truetype("Arial Unicode.ttf", 16))
    # combine img and txt
    combined = Image.alpha_composite(img, txtImg)
    combined.save(f'{path}/{fileName}')
    return jsonify({'success': True, 'msg': 'success'})


LocationArray = []
if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='127.0.0.1', port='40129', debug=True, use_reloader=False)
    # app.run(host='140.134.79.128', port='40129', use_reloader=False)
    # app.run(host='140.116.152.77', port='40129', debug=True, use_reloader=False)
