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
            'bronze': 0,
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
