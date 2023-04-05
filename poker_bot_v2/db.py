import os
import json
import datetime
import dotenv
import pymongo
from bson.objectid import ObjectId

# DB接続
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
url:str = os.environ['DB_CONNECTION_STRING']
client = pymongo.MongoClient(url)

# コレクション定義
db = client['pokerbotv2']
players = db['players']
backups = db['backups']


# accountをnameに変換
def account_to_name(name_or_account:str) -> str:
    player = players.find_one({'account': name_or_account})
    if player:
        return player['name']
    else:
        return name_or_account

# nameをaccountに変換
def name_to_account(name:str) -> str:
    player = players.find_one({'name': name})
    if player['account'] != '':
        return player['account']
    else:
        return name

# プレイヤーが存在しているかチェック
def exist_check(name:str) -> bool:
    player:bool = players.find_one({'name': name})
    if player:
        return True
    else:
        return False

# プレイヤーのレートを取得
def get_rate(name:str) -> int:
    player = players.find_one({'name': name})
    return player['rate']

# プレイヤーの参加回数を取得
def get_game(name:str) -> int:
    player = players.find_one({'name': name})
    return player['game']

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

# ランキング取得
def get_ranking(limit) -> list[dict]:
    results = list(players.find())
    for i in range(len(results)-1):
        for j in range(i+1, len(results)):
            if results[i]['rate'] < results[j]['rate']:
                results[i], results[j] = results[j], results[i]
    return results[:limit]


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
            'game': 0,
            'first': 0,
            'second': 0,
            'third': 0,
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


# プレイヤーデータを更新
def update_player(name:str, rate:int, game:int, first:int, second:int, third:int):
    query:dict = {'name': name}
    change:dict = {'$set': {
        'rate': rate,
        'game': game,
        'first': first,
        'second': second,
        'third': third
    }}
    players.update_one(query, change)


# バックアップ作成
def create_backup():
    data:list[dict] = list(players.find())
    backup:dict = {
        'data': str(data),
        'time': datetime.datetime.utcnow()
    }
    post_id:int = backups.insert_one(backup).inserted_id
    return post_id


# バックアップから復元
def rollback(backup_id:str) -> str:
    result:str = backups.find_one({'_id': ObjectId(backup_id)})
    if not result:
        return 'backup is not found!'
    else:
        players.delete_many({})
        backup:dict = json.loads(result['data'].replace('\'', '\"').replace('ObjectId(', '').replace(')', ''))
        for data in backup:
            data['_id'] = ObjectId(data['_id'])
            players.insert_one(data)
        return 'rollback successful!'