import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands
from datetime import date


with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)


class Authkey(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="authkey", description="Links your authkey")
    @app_commands.describe(authkey="Authkey")
    async def authkey(self,interaction: discord.Interaction, authkey: str):
        for name in db["Users"]:
                if name["User_ID"] == interaction.user.id:
                    name["Authkey"] = authkey
                    name["Authkey_lastupdate"] = str(date.today())
                    await interaction.response.send_message("Authkey set! Remember that your authkey changes every 24 hours, so be sure to update it soon!")
                    isin=True
                    break
                else:
                    isin=False

        if isin==False:
            db["Users"].append({"User_ID":interaction.user.id,
                                "User_name":interaction.user.name,
                                "ltuid":"",
                                "ltoken":"",
                                "UID":"",
                                "Resin":False,
                                "Realm_currency":False,
                                "Resin_pinged":False,
                                "Realm_pinged":False,
                                "Authkey":authkey,
                                "Authkey_lastupdate":str(date.today())
                                    })
            await interaction.response.send_message("Authkey set! Remember that your authkey changes every 24 hours, so be sure to update it soon!")

async def setup(bot):
    await bot.add_cog(Authkey(bot))