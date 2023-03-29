import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

def main():
    
    # 環境変数取得
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']

    # Botオブジェクト生成
    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())


    # オンライン確認用
    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')


    # Bot起動
    bot.run(TOKEN)


if __name__ == '__main__':
    main()