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

class Wish_History(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="wish_history", description="Shows your wish history")
    async def wishhistory(self,interaction: discord.Interaction):
        try:
            for name in db["Users"]:
                if name["User_ID"] == interaction.user.id:
                    url = name["Authkey"]
                    authkey = genshin.utility.extract_authkey(url)
                    client.authkey = authkey
                    pages = [discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes"),discord.Embed(title=f"{interaction.user.name}'s Wishes")]
                    pages[0].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
                    pages[1].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
                    pages[2].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
                    pages[3].set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png/revision/latest?cb=20201117073436")
                    pages[0].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}. Data for {name['Authkey_lastupdate']}")
                    pages[1].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}. Data for {name['Authkey_lastupdate']}")
                    pages[2].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}. Data for {name['Authkey_lastupdate']}")
                    pages[3].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}. Data for {name['Authkey_lastupdate']}")
            
                    i=0
                    await interaction.response.defer()
                    await asyncio.sleep(3)
                    async for wish in client.wish_history([301],limit=96):
                        if i<24:
                            i+=1
                            pages[0].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")

                        elif i>=24 and i<48:
                            i+=1
                            pages[1].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")

                        elif i>=48 and i<72:
                            i+=1
                            pages[2].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")
                        
                        else:
                            i+=1
                            pages[3].add_field(name=f"{i}. {wish.name}", value = f"({wish.rarity}* {wish.type})")
                            break
                    await interaction.followup.send(embed=pages[0],view = ButtonMenu(pages,60))
        except KeyError:
            await interaction.followup.send("You have to set an authkey! (type /help authkey)")
        except genshin.errors.AuthkeyTimeout:
            await interaction.followup.send("Your authkey has timed out! Type /authkey to set a new one")
        except RuntimeError:
            await interaction.followup.send("Your authkey is wrong! Try linking your authkey once again. For tutorial type /help authkey")

async def setup(bot):
    await bot.add_cog(Wish_History(bot))