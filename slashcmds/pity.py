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


class Pity(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="pity", description="Pity counter")
    async def pity(self,interaction: discord.Interaction):
        await interaction.response.defer()
        await asyncio.sleep(3)
        try:
            for name in db["Users"]:
                    if name["User_ID"] == interaction.user.id:
                        url = name["Authkey"]
                        authkey = genshin.utility.extract_authkey(url)
                        client.authkey = authkey
                        standard = 0
                        banner = 0
                        weapon = 0
                        async for wish in client.wish_history(genshin.models.BannerType.STANDARD):
                            if wish.rarity < 5:
                                standard += 1
                            else:
                                break

                        async for wish in client.wish_history(genshin.models.BannerType.WEAPON):
                            if wish.rarity < 5:
                                weapon += 1
                            else:
                                break

                        async for wish in client.wish_history(genshin.models.BannerType.CHARACTER):
                            if wish.rarity < 5:
                                banner += 1
                            else:
                                break

                        embed = discord.Embed(title=f"{interaction.user.name}'s Pity")
                        embed.set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Item_Primogem.png/revision/latest?cb=20201117071158")
                        embed.set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}. Data for {name['Authkey_lastupdate']}")
                        embed.add_field(name="Event banner: ",value = banner, inline=False)
                        embed.add_field(name="Standard: ",value = standard, inline=False)
                        embed.add_field(name="Weapon: ",value = weapon, inline=False)
                        await interaction.followup.send(embed=embed)
                        isin = True
                        break
                    else:
                        isin = False
            if isin == False:
                await interaction.followup.send("You have to set an authkey! (type /help authkey)")
        except KeyError:
            await interaction.followup.send("You have to set an authkey! (type /help authkey)")
        except genshin.errors.AuthkeyTimeout:
            await interaction.followup.send("Your authkey has timed out! Type /authkey to set a new one")
        except RuntimeError:
            await interaction.followup.send("Your authkey is wrong! Try linking your authkey once again. For tutorial type /help authkey")

async def setup(bot):
    await bot.add_cog(Pity(bot))