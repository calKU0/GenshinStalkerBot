import discord
import genshin
import asyncio
from discord import app_commands
from discord.ext import commands, tasks
import json
from replit import Database
import genshinstats as gs
from MenuButtons import ButtonMenu


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
print(db["Users"])


@bot.event
async def on_ready():
    task_loop.start()
    pinging_loop.start()
    print("We've logged in as {0.user}".format(bot))
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
        print(db["Users"])
        print("looped2")


#Registering a user
@bot.tree.command(name="link", description="link your genshin account")
@app_commands.describe(ltuid_cookie="Input your luid cookie")
@app_commands.describe(ltoken_cookie="Input your ltoken cookie")
@app_commands.describe(uid="Input your UID")
async def link(interaction: discord.Interaction, ltuid_cookie: str, ltoken_cookie: str, uid: str):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            await interaction.response.send_message("You are already registered!")
            isin=True
            break
        else:
            isin=False

    if isin==False:
        db["Users"].append({"User_ID":interaction.user.id,
                            "User_name":interaction.user.name,
                            "ltuid":ltuid_cookie,
                            "ltoken":ltoken_cookie,
                            "UID":uid,
                            "Resin":False,
                            "Realm_currency":False,
                            "Resin_pinged":False,
                            "Realm_pinged":False
                                })
        await interaction.response.send_message("Succesfully registered!")
    print(db["Users"])


@bot.tree.command(name="profile", description="Your profile stats")
async def profile(interaction: discord.Interaction):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            cookie(interaction.user.id)
            stats = gs.get_user_stats(name["UID"])["stats"]
            embed = discord.Embed(title=f"{interaction.user.name}'s Profile")
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            await interaction.response.defer(ephemeral=False)
            await asyncio.sleep(10)
            for field, valuee in stats.items():
                embed.add_field(name = str(field), value = str(valuee))
            await interaction.followup.send(embed=embed)
            isin = True
            break
        else:
            isin = False
    if isin == False:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="characters", description="Your characters information")
async def characters(interaction: discord.Interaction):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            cookie(interaction.user.id)
            characters = gs.get_characters(name["UID"])
            pages = [discord.Embed(title=f"{interaction.user.name}'s Characters"),discord.Embed(title=f"{interaction.user.name}'s Characters page 2")]
            pages[0].set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
            pages[0].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            pages[1].set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
            pages[1].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            i=0
            for char in characters:
                if i<24:
                    i+=1
                    pages[0].add_field(name=f"{char['name']:10}", value = f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}", inline=True)
                else:
                    pages[1].add_field(name=f"{char['name']:10}", value = f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}", inline=True)
                
            await interaction.response.send_message(embed=pages[0],view = ButtonMenu(pages,60))
            isin = True
            break
        else:
            isin = False
    if isin == False:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="abbys", description="Your characters abbys stats")
async def abbys(interaction: discord.Interaction):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            cookie(interaction.user.id)
            stats = gs.get_spiral_abyss(name["UID"], previous=True)["stats"]
            embed = discord.Embed(title=f"{interaction.user.name}'s Abbys Stats")
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            embed.set_image(url="https://static.wikia.nocookie.net/gensin-impact/images/c/ca/Domain_Spiral_Abyss_Abyssal_Moon_Spire.png/revision/latest?cb=20210326011346")
            for field, valuee in stats.items():
                embed.add_field(name = str(field), value = str(valuee),inline=True)
            await interaction.response.send_message(embed=embed)
            isin = True
            break
        else:
            isin = False
    if isin == False:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="resources", description="Your Resources")
async def resources(interaction: discord.Interaction):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            cookie(interaction.user.id)
            notes = gs.get_notes(name["UID"])
            embed = discord.Embed(title=f"{interaction.user.name}'s resources")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png/revision/latest?cb=20210106074218")
            embed.add_field(name="Current resin: ",value =f"{notes['resin']}/{notes['max_resin']}")
            embed.add_field(name="Current realm currency: ",value =f"{notes['realm_currency']}/{notes['max_realm_currency']}")
            embed.add_field(name="Expeditions: ",value =f"{len(notes['expeditions'])}/{notes['max_expeditions']}")
            embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
            isin=True
            print(type(notes['resin']))
            break
        else:
            isin = False
    if isin == False:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="notifications", description="Notify me when my resources are full")
@app_commands.choices(notifications = [app_commands.Choice(name="Resin",value="1"), app_commands.Choice(name="Realm currency",value="0")])
async def notifications(interaction: discord.Interaction,notifications: app_commands.Choice[str]):
    if notifications.value == "1":
        for name in db["Users"]:
            if name["User_ID"] == interaction.user.id:
                name["Resin"] = True
                await interaction.response.send_message("Successfully signed!")
                isin = True
                break
            else:
                isin = False
        if isin == False:
            await interaction.response.send_message("You have to register! (type /link)")
    else:
        for name in db["Users"]:
            if name["User_ID"] == interaction.user.id:
                name["Realm_currency"] = True
                await interaction.response.send_message("Successfully signed!")
                isin = True
                break
            else:
                isin = False
        if isin == False:
            await interaction.response.send_message("You have to register! (type /link)")


@bot.tree.command(name="daily", description="Claim your daily rewards")
async def notifications(interaction: discord.Interaction):
    for name in db["Users"]:
        if name["User_ID"] == interaction.user.id:
            genshincookies(interaction.user.id)
            try:
                reward = await client.claim_daily_reward()
            except genshin.AlreadyClaimed:
                await interaction.response.send_message("Daily reward already claimed")
                break
            else:
                await interaction.response.send_message(f"Claimed {reward.amount}x {reward.name}")
                isin = True
                break
        else:
            isin = False
        if isin == False:
            await interaction.response.send_message("You have to register! (type /register)")


@bot.tree.command(name="wish_history", description="Shows your wish history")
async def notifications(interaction: discord.Interaction):
    client.authkey = genshin.utility.get_authkey()
    pages = [discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes")]
    pages[0].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
    pages[1].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
    pages[2].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
    pages[3].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
    pages[0].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
    pages[1].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
    pages[2].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
    pages[3].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
    
    i=0
    await interaction.response.defer()
    await asyncio.sleep(7)
    async for wish in client.wish_history([301],limit=96):
        if i<24:
            i+=1
            pages[0].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")

        elif i>=24 and i<48:
            i+=1
            pages[1].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")

        elif i>=48 and i<72:
            i+=1
            pages[2].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")
        
        else:
            i+=1
            pages[3].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")
                
    await interaction.followup.send(embed=pages[0],view = ButtonMenu(pages,60))

bot.run(TOKEN)

