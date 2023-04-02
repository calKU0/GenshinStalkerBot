import discord
from discord.ext import commands
import json
import os
from loops import notifications_ping, pinged_check, auto_daily

with open("config.json") as config:
    content = json.load(config)
    TOKEN = content["DISCORD_TOKEN"]
    DATABASE = content["DATABASE"]

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 

@bot.event
async def on_ready():
    notifications_ping.start()
    pinged_check.start()
    auto_daily.start()
    print("We've logged in as {0.user}".format(bot))
    for filename in os.listdir('./slashcmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f"slashcmds.{filename[:-3]}")
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(TOKEN)

