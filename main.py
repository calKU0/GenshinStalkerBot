import discord
from discord.ext import commands
import json
import os
import loops
import inspect

with open("config.json") as config:
    content = json.load(config)
    TOKEN = content["DISCORD_TOKEN"]
    DATABASE = content["DATABASE"]

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 



@bot.event
async def on_ready():
    # Loop through all symbols in the loops module and start any functions with a start() method
    for name in inspect.getmembers(loops):
        if inspect.iscoroutinefunction(name):
            name.start()

    for filename in os.listdir('./slashcmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f"slashcmds.{filename[:-3]}")

    await bot.change_presence(activity=discord.Game(name="Genshin Impact"))
    print("We've logged in as {0.user}".format(bot))
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(TOKEN)

