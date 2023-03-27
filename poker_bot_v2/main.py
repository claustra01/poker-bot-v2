import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from player import Player
from medals import Medals
import utils

def main():
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']

    bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())
    db:list[Player] = []

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello!')

    @bot.command()
    async def register(ctx, *key_and_id):
        key:str = key_and_id[0]
        id:str = key_and_id[1] if len(key_and_id) > 1 else None
        player:Player = Player(id, key, 1500, Medals(0, 0, 0))
        db.append(player)
        await ctx.send(key + ' is registered!')

    @bot.command()
    async def link(ctx, key, id):
        player:Player = utils.key_to_player(db, key)
        if player == None:
            await ctx.send(key + " is not found!")
        player.set_id(id)
        await ctx.send(id + ' is linked!')

    bot.run(TOKEN)

if __name__ == '__main__':
    main()