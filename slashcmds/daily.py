import discord
import json
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

class Daily(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        

    @app_commands.command(name="daily", description="Claim your daily rewards")
    async def daily(self,interaction: discord.Interaction):
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
            await interaction.response.send_message("You have to link your hoyolab account! (type `/link help)`")

async def setup(bot):
    await bot.add_cog(Daily(bot))