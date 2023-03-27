import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

from player import Player
from medals import Medals
import utils

def main():
    
    # TOKEN取得
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']

    # Botオブジェクト生成
    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())

    # 疑似DB生成
    db:list[Player] = []


    # オンライン確認用
    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')

    
    # Rating表示


    # ランキング表示


    # プレイヤー登録
    @bot.command()
    @commands.has_role("Promoter")
    async def register(ctx, *key_and_id):
        key:str = key_and_id[0]
        id:str = key_and_id[1] if len(key_and_id) > 1 else None
        player:Player = Player(id, key, 1500, Medals(0, 0, 0))
        db.append(player)
        await ctx.send(key + ' is registered!')


    # Discordアカウント紐付け
    @bot.command()
    @commands.has_role("Promoter")
    async def link(ctx, key, id):
        player:Player = utils.key_to_player(db, key)
        if player == None:
            await ctx.send(key + " is not found!")
        player.set_id(id)
        await ctx.send(id + ' is linked!')


    # 結果入力


    # DB全出力
    @bot.command()
    @commands.has_role("Promoter")
    async def export(ctx):
        obj:list[str] = []
        for i in range(len(db)):
            obj.append(db[i].get_data())
        await ctx.send('```' + str(obj).replace(' ', '').replace("\'", "\\\"") + '```')


    # DB上書き
    @bot.command()
    @commands.has_role("Promoter")
    async def override(ctx, data):
        db.clear()
        obj:dict = json.loads(data)
        for i in range(len(obj)):
            id:str = obj[i]['id'] if obj[i]['id'] != '' else None
            key:str = obj[i]['key']
            rating:int = obj[i]['rating']
            medals:Medals = Medals(obj[i]['medals']['gold'], obj[i]['medals']['silver'], obj[i]['medals']['bronze'])
            player:Player = Player(id, key, rating, medals)
            db.append(player)
        await ctx.send('override successful!')


    # Bot起動
    bot.run(TOKEN)


if __name__ == '__main__':
    main()