from Cookies import cookie
import discord
import json
import asyncio
from replit import Database
from discord import app_commands
from discord.ext import commands
import genshinstats as gs

with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)


class Profile(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Your profile stats")
    async def profile(self,interaction: discord.Interaction):
        for name in db["Users"]:
            if name["User_ID"] == interaction.user.id:
                cookie(interaction.user.id)
                stats = gs.get_user_stats(name["UID"])["stats"]
                embed = discord.Embed(title=f"{interaction.user.name}'s Profile")
                embed.set_thumbnail(url=interaction.user.avatar.url)
                embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
                await interaction.response.defer(ephemeral=False)
                await asyncio.sleep(3)
                for field, valuee in stats.items():
                    embed.add_field(name = str(field), value = str(valuee))
                await interaction.followup.send(embed=embed)
                isin = True
                break
            else:
                isin = False
        if isin == False:
            await interaction.response.send_message("You have to register! (type /register)")

async def setup(bot):
    await bot.add_cog(Profile(bot))