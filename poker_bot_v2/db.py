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
    result = players.find_one({'name': name})
    if result:
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
        return 'OK'
    

# テストPOST
print(create_player('a', 'aa'))
