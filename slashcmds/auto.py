import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands


with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

class Auto(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="auto", description="Redeems your daily rewards automatically every 24 hours")
    @app_commands.choices(type = [app_commands.Choice(name="daily",value="1")])
    async def auto(self,interaction: discord.Interaction,type: app_commands.Choice[str]):
        if type.value == "1":
            for name in db["Users"]:
                if name["User_ID"] == interaction.user.id:
                    try:
                        if name["Auto_daily"] == True:
                            name["Auto_daily"] = False
                            await interaction.response.send_message("Succesfully unsigned. From now on you won't get your daily rewards automatically")
                            isin = True
                            break
                        else:
                            name["Auto_daily"] = True
                            await interaction.response.send_message("Succesfully signed. From now on you will get your daily rewards every 24 hours")
                            isin = True
                            break
                    except KeyError:
                            name["Auto_daily"] = True
                            await interaction.response.send_message("Succesfully signed. From now on you will get your daily rewards every 24 hours")
                            isin = True
                            break
                else:
                    isin = False
            if isin == False:
                await interaction.response.send_message("You have to link your hoyolab account! (type `/link help)`")

async def setup(bot):
    await bot.add_cog(Auto(bot))