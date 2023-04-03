import os
import datetime
import dotenv
import pymongo

# DB接続
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
url:str = os.environ['DB_CONNECTION_STRING']
client = pymongo.MongoClient(url)

# コレクション定義
db = client['pokerbotv2']
players = db['players']
backups = db['backups']


# プレイヤーデータ作成
def create_player(name:str, account:str) -> str:
    exist_name = players.find_one({'name': name})
    if exist_name:
        return name + ' is already exist!'
    else:
        data:dict = {
            'name': name,
            'account': account,
            'rate': 1500,
            'first': 0,
            'second': 0,
            'third': 0,
            'time': datetime.datetime.utcnow()
        }
        players.insert_one(data)
        return name + ' is registered!'
    

# アカウント紐付け
def link_account(name:str, account:str) -> str:
    exist_name = players.find_one({'name': name})
    exist_account = players.find_one({'account': account})
    if exist_name and not exist_account:
        query:dict = {'name': name}
        change:dict = {'$set': {'account': account}}
        players.update_one(query, change)
        return account + ' is linked!'
    elif exist_name and exist_account:
        return account + ' is already linked!'
    else:
        return name + ' is not found!'


# 存在しないプレイヤーのリストを取得
def get_undefined_name(names:tuple) -> list[str]:
    not_exists:list[str] = []
    for i in range(len(names)):
        exist_name = players.find_one({'name': names[i]})
        if not exist_name:
            not_exists.append(names[i])
    return not_exists

# プレイヤーのレートを取得
def get_rate(name:str) -> int:
    player = players.find_one({'name': name})
    return player['rate']

# プレイヤーの1位回数を取得
def get_first(name:str) -> int:
    player = players.find_one({'name': name})
    return player['first']

# プレイヤーの2位回数を取得
def get_second(name:str) -> int:
    player = players.find_one({'name': name})
    return player['second']

# プレイヤーの3位回数を取得
def get_third(name:str) -> int:
    player = players.find_one({'name': name})
    return player['third']

# プレイヤーデータを更新
def update_player(name:str, rate:int, first:int, second:int, third:int):
    query:dict = {'name': name}
    change:dict = {'$set': {
        'rate': rate,
        'first': first,
        'second': second,
        'third': third
    }}
    players.update_one(query, change)
