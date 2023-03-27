import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands


with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

class Notifications(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="notifications", description="Notify me when my resources are full")
    @app_commands.choices(notifications = [app_commands.Choice(name="Resin",value="1"), app_commands.Choice(name="Realm currency",value="0")])
    async def notifications(self,interaction: discord.Interaction,notifications: app_commands.Choice[str]):
        if notifications.value == "1":
            for name in db["Users"]:
                if name["User_ID"] == interaction.user.id:
                    if name["Resin"] == False:
                        name["Resin"] = True
                        await interaction.response.send_message("Successfully signed!")
                        isin = True
                        break
                    else:
                        name["Resin"] = False
                        await interaction.response.send_message("Successfully unsigned!")
                        isin = True
                        break
                else:
                    isin = False
            if isin == False:
                await interaction.response.send_message("You have to link your hoyolab account! (type `/link help)`")
        else:
            for name in db["Users"]:
                if name["User_ID"] == interaction.user.id:
                    if name["Realm_currency"] == False:
                        name["Realm_currency"] = True
                        await interaction.response.send_message("Successfully signed!")
                        isin = True
                        break
                    else:
                        name["Realm_currency"] = False
                        await interaction.response.send_message("Successfully unsigned!")
                        isin = True
                        break
                else:
                    isin = False
            if isin == False:
                await interaction.response.send_message("You have to link your hoyolab account! (type `/link help)`")

async def setup(bot):
    await bot.add_cog(Notifications(bot))