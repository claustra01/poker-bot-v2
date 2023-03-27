import os
import json
import cryptocode
import discord
from discord.ext import commands
from dotenv import load_dotenv

from player import Player
from medals import Medals
import utils

def main():
    
    # 環境変数取得
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    KEY = os.environ['CRYPTO_KEY']

    # Botオブジェクト生成
    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())

    # 疑似DB生成
    db:list[Player] = []


    # オンライン確認用
    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')

    
    # Rating表示
    @bot.command()
    async def rating(ctx, id_or_key):
        key:str = utils.id_to_key(db, id_or_key)
        if not utils.exist_check(db, key):
            await ctx.send(key + ' is not found!')
            return
        
        player:Player = utils.key_to_player(db, key)
        await ctx.send(player.get_name() + '\'s rating: ' + str(player.get_rating()) + 'pt')

        emojis:str = ''
        for i in range(player.get_medals().get_gold()):
            emojis += ':first_place:'
        for i in range(player.get_medals().get_silver()):
            emojis += ':second_place:'
        for i in range(player.get_medals().get_bronze()):
            emojis += ':third_place:'
        if emojis != '':
            await ctx.send(player.get_name() + '\'s medals: ' + emojis)


    # ランキング表示
    @bot.command()
    async def ranking(ctx, limit):
        utils.sort_by_rating(db)
        for i in range(min(10, int(limit), len(db))):
            await ctx.send(db[i].get_name() + ' ' + str(db[i].get_rating()) + 'pt')


    # プレイヤー登録
    @bot.command()
    async def register(ctx, *key_and_id):
        key:str = key_and_id[0]
        id:str = key_and_id[1] if len(key_and_id) > 1 else None
        if utils.exist_check(db, key):
            await ctx.send(key + ' is already exist!')
            return
        player:Player = Player(id, key, 1500, Medals(0, 0, 0))
        db.append(player)
        await ctx.send(key + ' is registered!')


    # Discordアカウント紐付け
    @bot.command()
    async def link(ctx, key, id):
        if not utils.exist_check(db, key):
            await ctx.send(key + ' is not found!')
            return
        player:Player = utils.key_to_player(db, key)
        player.set_id(id)
        await ctx.send(id + ' is linked!')


    # 結果入力
    @bot.command()
    async def result(ctx, member, stack, *players):        
        if int(member) != len(players):
            await ctx.send('missing arguments!')
            return
        
        if len(players) <= 2:
            await ctx.send('heads up is not supported!')
            return
        
        keys:list[str] = []
        not_exist:list[str] = []
        for i in range(len(players)):
            keys.append(utils.id_to_key(db, players[i]))
            if not utils.exist_check(db, keys[i]):
                not_exist.append(keys[i])
        if not_exist != []:
            for i in range(len(not_exist)):
                await ctx.send(not_exist[i] + ' is not found!')
            return
        
        for i in range(len(keys)):
            player:Player = utils.key_to_player(db, keys[i])
            rating:int = player.get_rating()
            rate_adds:float = 0
            for j in range(len(keys)):
                if i != j:
                    opp_rate:int = utils.key_to_player(db, keys[j]).get_rating()
                    if i < j:
                        rate_adds += utils.calc_rate_adds(int(stack), rating, opp_rate)
                    else:
                        rate_adds -= utils.calc_rate_adds(int(stack), opp_rate, rating)
            player.set_rating(round(rating + rate_adds))

        g_player:Player = utils.key_to_player(db, keys[0])
        g_medals:Medals = g_player.get_medals()
        g_medals.add_gold()
        g_player.set_medals(g_medals)
        s_player:Player = utils.key_to_player(db, keys[1])
        s_medals:Medals = s_player.get_medals()
        s_medals.add_silver()
        s_player.set_medals(s_medals)
        b_player:Player = utils.key_to_player(db, keys[2])
        b_medals:Medals = b_player.get_medals()
        b_medals.add_bronze()
        b_player.set_medals(b_medals)
        await ctx.send('rating updated!')


    # DB全出力
    @bot.command()
    async def export(ctx):
        obj:list[str] = []
        for i in range(len(db)):
            obj.append(db[i].get_data())
        raw:str = str(obj).replace(' ', '').replace('\'', '\"')
        await ctx.send('```' + cryptocode.encrypt(raw, KEY) + '```')


    # DB上書き
    @bot.command()
    async def override(ctx, data):
        db.clear()
        obj:dict = json.loads(cryptocode.decrypt(data, KEY))
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