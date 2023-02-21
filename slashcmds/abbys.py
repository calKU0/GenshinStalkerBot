import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands
import genshinstats as gs

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

class Abbys(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="abbys", description="Your characters abbys stats")
    async def abbys(self,interaction: discord.Interaction):
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

async def setup(bot):
    await bot.add_cog(Abbys(bot))