import discord
import genshin
import os
import asyncio
from discord import app_commands
from discord.ext import commands
import json
from replit import Database
import genshinstats as gs

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
        index = list(db["Users"]["User_ID"]).index(str(interaction.user.id))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        stats = gs.get_user_stats(db["Users"]["UID"][index])['stats']
        embed = discord.Embed(title=f"{interaction.user.name}'s Profile")
        embed.set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
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
        index = list(db["Users"]["User_ID"]).index(str(interaction.user.id))
        gs.set_cookie(ltuid=db["Users"]["ltuid"][index], ltoken=db["Users"]["ltoken"][index])
        characters = gs.get_characters(db["Users"]["UID"][index])
        embed = discord.Embed(title=f"{interaction.user.name}'s characters")
        embed.set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
        await interaction.response.defer(ephemeral=False)
        await asyncio.sleep(10)
        j = 0
        for char in characters:
            j += 1
            if j % 25 != 0 and j<25:
                embed.add_field(name={char['name']:10}, value = f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}")
                
            else:
                if j % 25 == 0:
                    await interaction.followup.send(embed=embed)
                    embed = discord.Embed(
                    colour = discord.Colour.blue()
                    )

            if j > 25 and (j % 25 != 0):
                await interaction.response.defer(ephemeral=False)
                await asyncio.sleep(5)
                embed.add_field(name={char['name']:10}, value=f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}")
            await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message("You have to register! (type /register)")

bot.run(TOKEN)

