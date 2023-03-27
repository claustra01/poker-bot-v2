import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

def main():
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']

    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')
    
    bot.run(TOKEN)

if __name__ == '__main__':
    main()