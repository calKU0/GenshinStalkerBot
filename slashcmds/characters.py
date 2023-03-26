import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands
import genshinstats as gs
from MenuButtons import ButtonMenu
from Cookies import cookie


with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

class Characters(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="characters", description="Your characters information")
    async def characters(self,interaction: discord.Interaction):
        for name in db["Users"]:
            if name["User_ID"] == interaction.user.id:
                cookie(interaction.user.id)
                characters = gs.get_characters(name["UID"])
                pages = [discord.Embed(title=f"{interaction.user.name}'s Characters"),discord.Embed(title=f"{interaction.user.name}'s Characters page 2")]
                pages[0].set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
                pages[0].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
                pages[1].set_thumbnail(url="https://pbs.twimg.com/media/E99MNCzVkAY-1V8?format=jpg&name=small")
                pages[1].set_footer(icon_url = interaction.user.avatar.url ,text=f"Requested by {interaction.user.name}")
                i=0
                for char in characters:
                    if i<24:
                        i+=1
                        pages[0].add_field(name=f"{char['name']:10}", value = f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}", inline=True)
                    else:
                        pages[1].add_field(name=f"{char['name']:10}", value = f"{char['rarity']}* | lvl {char['level']:2} C{char['constellation']}", inline=True)
                    
                await interaction.response.send_message(embed=pages[0],view = ButtonMenu(pages,60))

                isin = True
                break
            else:
                isin = False
        if isin == False:
            await interaction.response.send_message("You have to register! (type /register)")

async def setup(bot):
    await bot.add_cog(Characters(bot))