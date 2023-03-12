import sys
sys.path.append('./modules')
from Cookies import cookie
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


class Resources(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @app_commands.command(name="resources", description="Your Resources")
    async def resources(self,interaction: discord.Interaction):
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

async def setup(bot):
    await bot.add_cog(Resources(bot))