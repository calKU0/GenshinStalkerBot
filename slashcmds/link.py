import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands


with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

class Link(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @app_commands.command(name="link", description="link your genshin account")
    @app_commands.describe(ltuid_cookie="Input your luid cookie")
    @app_commands.describe(ltoken_cookie="Input your ltoken cookie")
    @app_commands.describe(uid="Input your UID")
    async def link(self,interaction: discord.Interaction, ltuid_cookie: str, ltoken_cookie: str, uid: str):
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

async def setup(bot):
    await bot.add_cog(Link(bot))