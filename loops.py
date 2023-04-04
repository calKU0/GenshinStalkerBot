import discord
import genshin
from discord.ext import commands, tasks
import json
from replit import Database
import genshinstats as gs
from Cookies import cookie

with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]

db = Database(db_url=DATABASE)
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 
client = genshin.Client(game=genshin.Game.GENSHIN)

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

@tasks.loop(hours = 7)
async def pinged_check():
    for name in db["Users"]:
        try:
            cookie(name["User_ID"])
            notes = gs.get_notes(name["UID"])
            if name["Resin_pinged"] and notes['resin'] < notes['max_resin']:
                name["Resin_pinged"] = False
            if name["Realm_pinged"] and notes["realm_currency"] < notes['max_realm_currency']:
                name["Realm_pinged"] = False
        except KeyError:
            continue
    print("looped2")

@tasks.loop(minutes=15)
async def notifications_ping():
    channel = bot.get_channel(1064465950511992865)
    for name in db["Users"]:
        try:
            if name["Resin"] and name["Resin_pinged"] == False:
                cookie(name["User_ID"])
                notes = gs.get_notes(name["UID"])
                if notes['resin'] >= notes['max_resin']:
                    await channel.send(f"<@{name['User_ID']}> Your resin is full!")
                    name["Resin_pinged"] = True
            if name["Realm_currency"] and name["Realm_pinged"] == False:
                cookie(name["User_ID"])
                notes = gs.get_notes(name["UID"])
                if notes['realm_currency'] >= notes['max_realm_currency']:
                    await channel.send(f"<@{name['User_ID']}> Your realm currency is full!")
                    name["Realm_pinged"] = True
        except KeyError:
            continue
    print("looped")

@tasks.loop(hours=24)
async def auto_daily():
    for name in db["Users"]:
        try:
            if name["Auto_daily"]:
                genshincookies(name["User_ID"])
                try:
                    await client.claim_daily_reward()
                except genshin.AlreadyClaimed:
                    continue
        except KeyError:
            continue
    print("looped3")