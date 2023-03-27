import discord
import json
import asyncio
import genshin
from replit import Database
from discord import app_commands
from discord.ext import commands

client = genshin.Client(game=genshin.Game.GENSHIN)

with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

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

class Diary(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="diary", description="Shows your earned primos")
    async def diary(self,interaction: discord.Interaction):
        for name in db["Users"]:
            if name["User_ID"] == interaction.user.id:
                await interaction.response.defer()
                await asyncio.sleep(3)
                genshincookies(interaction.user.id)
                diary = await client.get_diary()
                embed = discord.Embed(title=f"{interaction.user.name}'s primogems earned this month: {diary.data.current_primogems}")
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Item_Primogem.png/revision/latest?cb=20201117071158")
                embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
                for category in diary.data.categories:
                    embed.add_field(name=f"{category.name}: ",value =f"{category.amount} primogems ({category.percentage}%)", inline=False)
                    #print(f"{category.percentage}% earned from {category.name} ({category.amount} primogems)")
                await interaction.followup.send(embed=embed)
                isin = True
                break
            else:
                isin = False
        if isin == False:
            await interaction.response.send_message("You have to link your hoyolab account! (type `/link help)`")

async def setup(bot):
    await bot.add_cog(Diary(bot))