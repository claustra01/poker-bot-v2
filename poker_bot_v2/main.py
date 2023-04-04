import os
import dotenv
import discord
from discord.ext import commands

import db
import utils

def main():
    
    # 環境変数取得
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    token = os.environ['DISCORD_BOT_TOKEN']

    # Botオブジェクト生成
    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())


    # オンライン確認用
    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')


    # レート表示
    @bot.command()
    async def rate(ctx, name_or_account):
        name:str = db.account_to_name(name_or_account)
        print(name)
        if not db.exist_check(name):
            await ctx.send(name + ' is not found!')
            return

        rate:int = db.get_rate(name)
        game:int = db.get_game(name)
        first:int = db.get_first(name)
        second:int = db.get_second(name)
        third:int = db.get_third(name)
        await ctx.send(
            db.name_to_account(name) + '\'s rate: ' + str(rate) + 'pt / ' + str(game) + 'game\n' +
            ':first_place:' * first + ':second_place:' * second + ':third_place:' * third
        )
    

    # ランキング表示
    @bot.command()
    async def ranking(ctx, limit):
        data:list(dict) = db.get_ranking(min(10, int(limit)))
        message:str = ''
        for player in data:
            message += (db.name_to_account(player['name']) + ' ' + str(player['rate']) + 'pt\n')
        await ctx.send(message)


    # プレイヤー登録
    @bot.command()
    async def register(ctx, *name_and_account):
        name:str = name_and_account[0]
        account:str = name_and_account[1] if len(name_and_account) > 1 else ''
        message:str = db.create_player(name, account)
        await ctx.send(message)

    
    # Discordアカウント紐付け
    @bot.command()
    async def link(ctx, name, account):
        message:str = db.link_account(name, account)
        await ctx.send(message)


    # 結果入力
    @bot.command()
    async def result(ctx, member, stack, *names):
        if int(member) != len(names):
            await ctx.send('missing arguments!')
            return        

        if len(names) <= 2:
            await ctx.send('heads up is not supported!')
            return
        
        not_exists:list[str] = db.get_undefined_name(names)
        if not_exists != []:
            for not_exist in not_exists:
                await ctx.send(not_exist + ' is not found!')
            return
        
        rates:list[int] = []
        for name in names:
            rates.append(db.get_rate(name))
        for i in range(len(names)):
            rate:int = rates[i]
            game:int = db.get_game(name)
            first:int = db.get_first(names[i])
            second:int = db.get_second(names[i])
            third:int = db.get_third(names[i])
            rate_adds:float = 0
            for j in range(len(names)):
                if i != j:
                    opp_rate:int = rates[j]
                    if i < j:
                        rate_adds += utils.calc_rate_adds(int(stack), rate, opp_rate)
                    else:
                        rate_adds -= utils.calc_rate_adds(int(stack), opp_rate, rate)
            rate += round(rate_adds) if rate_adds > 0 else round(rate_adds / 2)
            game += 1
            if i == 0:
                first += 1
            if i == 1:
                second += 1
            if i == 2:
                third += 1
            db.update_player(names[i], rate, game, first, second, third)
        await ctx.send('rating updated!')


    # バックアップ作成
    @bot.command()
    async def backup(ctx):
        backup_id = db.create_backup()
        await ctx.send('backup id: `' + str(backup_id) + '`')

    
    # バックアップから復元
    @bot.command()
    async def rollback(ctx, backup_id):
        message:str = db.rollback(backup_id)
        await ctx.send(message)


    # Bot起動
    bot.run(token)


if __name__ == '__main__':
    main()