import os
import dotenv
from pymongo import MongoClient
import datetime

# DB接続
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
url:str = os.environ['DB_CONNECTION_STRING']
client = MongoClient(url)

# コレクション定義
db = client['pokerbotv2']
players = db['players']
backups = db['backups']

# テストPOST
post = {
    "title": "Azure Cosmos DBにPythonから接続する",
    "body": "PythonでAzure Cosmos DBのMongoDB APIに接続してデータをポストする方法を学びました。",
    "author": "ChatGPT",
    "tags": ["Azure", "Cosmos DB", "Python"],
    "date": datetime.datetime.utcnow()
}
post_id = players.insert_one(post).inserted_id
print(post_id)
