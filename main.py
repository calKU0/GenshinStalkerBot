import discord
import genshin
import asyncio
from discord import app_commands
from discord import ui
from discord.ui import View
from discord.ext import commands
import json
from replit import Database
import genshinstats as gs
import typing
from MenuButtons import ButtonMenu




class getgenshin():
    def stats(self,user):
        index = list(db["Users"]["User_ID"]).index(str(user))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        return gs.get_user_stats(db["Users"]["UID"][index])['stats']
    def characters(self,user):
        index = list(db["Users"]["User_ID"]).index(str(user))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        return gs.get_characters(db["Users"]["UID"][index])
    def abbys(self,user):
        index = list(db["Users"]["User_ID"]).index(str(user))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        spiral_abyss = gs.get_spiral_abyss(db["Users"]["UID"][index], previous=True)
        return spiral_abyss['stats']
    def notes(self,user):
        index = list(db["Users"]["User_ID"]).index(str(user))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        return gs.get_notes(db["Users"]["UID"][index])


gg = getgenshin()

    


with open("config.json") as config:
    content = json.load(config)
    TOKEN = content["DISCORD_TOKEN"]
    DATABASE = content["DATABASE"]

db = Database(db_url=DATABASE)
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all()) 

@bot.event
async def on_ready():
  print("We've logged in as {0.user}".format(bot))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

#Registering a user
@bot.tree.command(name="link", description="link your genshin account")
@app_commands.describe(ltuid_cookie="Input your luid cookie")
@app_commands.describe(ltoken_cookie="Input your ltoken cookie")
@app_commands.describe(uid="Input your UID")
async def link(interaction: discord.Interaction, ltuid_cookie: str, ltoken_cookie: str, uid: str):
  if str(interaction.user.id) in db["Users"]["User_ID"]:
    await interaction.response.send_message("You are already registered!")
  else:
    db["Users"]["User_ID"].append(str(interaction.user.id))
    db["Users"]["ltuid"].append(ltuid_cookie)
    db["Users"]["ltoken"].append(ltoken_cookie)
    db["Users"]["UID"].append(uid)
    await interaction.response.send_message("Succesfully registered!")


@bot.tree.command(name="profile", description="Your profile stats")
async def profile(interaction: discord.Interaction):
    if str(interaction.user.id) in str(db["Users"]["User_ID"]).split("'"):
        stats = gg.stats(interaction.user.id)
        embed = discord.Embed(title=f"{interaction.user.name}'s Profile")
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
        await interaction.response.defer(ephemeral=False)
        await asyncio.sleep(10)
        for field, valuee in stats.items():
            embed.add_field(name = str(field), value = str(valuee))
        await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="characters", description="Your characters information")
async def characters(interaction: discord.Interaction):
    if str(interaction.user.id) in str(db["Users"]["User_ID"]).split("'"):
        characters = gg.characters(interaction.user.id)
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
        
    else:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="abbys", description="Your characters abbys stats")
async def abbys(interaction: discord.Interaction):
    if str(interaction.user.id) in str(db["Users"]["User_ID"]).split("'"):
        stats = gg.abbys(interaction.user.id)
        embed = discord.Embed
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
        embed.set_image(url="https://static.wikia.nocookie.net/gensin-impact/images/c/ca/Domain_Spiral_Abyss_Abyssal_Moon_Spire.png/revision/latest?cb=20210326011346")
        for field, valuee in stats.items():
            embed.add_field(name = str(field), value = str(valuee),inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You have to register! (type /register)")

@bot.tree.command(name="resources", description="Your Resources")
async def resources(interaction: discord.Interaction):
    if str(interaction.user.id) in str(db["Users"]["User_ID"]).split("'"):
        notes = gg.notes(interaction.user.id)
        embed = discord.Embed(title=f"{interaction.user.name}'s resources")
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png/revision/latest?cb=20210106074218")
        embed.add_field(name="Current resin: ",value =f"{notes['resin']}/{notes['max_resin']}")
        embed.add_field(name="Current realm currency: ",value =f"{notes['realm_currency']}/{notes['max_realm_currency']}")
        embed.add_field(name="Expeditions: ",value =f"{len(notes['expeditions'])}/{notes['max_expeditions']}")
        embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You have to register! (type /register)")


bot.run(TOKEN)

