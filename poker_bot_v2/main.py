import os
import dotenv
import discord
from discord.ext import commands

import db

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
        


    # Bot起動
    bot.run(token)


if __name__ == '__main__':
    main()