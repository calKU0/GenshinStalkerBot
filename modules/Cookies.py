import genshinstats as gs
from replit import Database
import json
import genshin

client = genshin.Client(game=genshin.Game.GENSHIN)

with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)


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