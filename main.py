import discord
import genshin
from discord.ext import commands, tasks
import json
from replit import Database
import genshinstats as gs
import os


client = genshin.Client(game=genshin.Game.GENSHIN)
def cookie(user):
    for name in db["Users"]:
        if name["User_ID"] == user:
            cookie = gs.set_cookie(ltuid=name["ltuid"], ltoken=name["ltoken"])
            isin=True
            break
        else:
            isin=False
        if isin==False:
            cookie = False
    return cookie

def genshincookies(user):
    for name in db["Users"]:
        if name["User_ID"] == user:
            cookie = client.set_cookies(ltuid=name["ltuid"], ltoken=name["ltoken"])
            isin=True
            break
        else:
            isin=False
        if isin==False:
            cookie = False
    return cookie
                


with open("config.json") as config:
    content = json.load(config)
    TOKEN = content["DISCORD_TOKEN"]
    DATABASE = content["DATABASE"]

db = Database(db_url=DATABASE)
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 



@bot.event
async def on_ready():
    task_loop.start()
    pinging_loop.start()
    await auto_daily()
    print("We've logged in as {0.user}".format(bot))
    for filename in os.listdir('./slashcmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f"slashcmds.{filename[:-3]}")
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@tasks.loop(minutes=15)
async def task_loop():
    channel = bot.get_channel(1064465950511992865)
    for name in db["Users"]:
        if name["Resin"] == True and name["Resin_pinged"] == False:
            cookie(name["User_ID"])
            notes = gs.get_notes(name["UID"])
            if notes['resin'] >= notes['max_resin']:
                await channel.send(f"<@{name['User_ID']}> Your resin is full!")
                name["Resin_pinged"] = True
        if name["Realm_currency"] == True and name["Realm_pinged"] == False:
            cookie(name["User_ID"])
            notes = gs.get_notes(name["UID"])
            if notes['realm_currency'] >= notes['max_realm_currency']:
                await channel.send(f"<@{name['User_ID']}> Your realm currency is full!")
                name["Realm_pinged"] = True
    print("looped")


@tasks.loop(hours = 7)
async def pinging_loop():
    for name in db["Users"]:
        cookie(name["User_ID"])
        notes = gs.get_notes(name["UID"])
        if name["Resin_pinged"] == True and notes['resin'] < notes['max_resin']:
            name["Resin_pinged"] = False
        if name["Realm_pinged"] == True and notes["realm_currency"] < notes['max_realm_currency']:
            name["Realm_pinged"] = False
    print("looped2")

@tasks.loop(hours=24)
async def auto_daily():
    for name in db["Users"]:
        try:
            if name["Auto_daily"] == True:
                genshincookies(name["User_ID"])
                try:
                    await client.claim_daily_reward()
                except genshin.AlreadyClaimed:
                    continue
        except KeyError:
            continue
    print("looped3")


bot.run(TOKEN)

