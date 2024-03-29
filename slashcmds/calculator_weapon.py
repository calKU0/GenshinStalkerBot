import discord
import json
import genshin
from discord import app_commands
from discord.ext import commands
import re
from Autocompletes import weapon_autocomplete

client = genshin.Client(game=genshin.Game.GENSHIN)

with open("config.json") as config:
    content = json.load(config)
    client.set_cookies(ltuid=content["GENSHIN_COOKIE1"], ltoken=content["GENSHIN_COOKIE2"])


class Calculator_weapon(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot  


    @app_commands.command(name="calculator_weapon",description="Calculates materials needed to upgrade your weapon")
    @app_commands.autocomplete(weapon=weapon_autocomplete)
    @app_commands.describe(current="Input your current lvl")
    @app_commands.describe(target="Input your target lvl")
    async def calculator_character(self,interaction: discord.Interaction, weapon: str, current: int, target: int):
        with open("data/weapons.json") as config:
            content = json.load(config)
            weaponid = content[weapon]

        builder = client.calculator()
        builder.set_weapon(weaponid, current=current, target=target)
        cost = await builder.calculate()
        name_amount_dict = {}

        for item in re.findall(r"name='([^']+)'.*?amount=(\d+)", str(cost)):
            name, amount = item
            name_amount_dict[name] = int(amount)

        embed = discord.Embed(title=f"Materials needed to upgrade {weapon} from level {current} to {target}",color=discord.Color.from_rgb(219, 42, 166))
        for key,val in name_amount_dict.items():
            #Searching the emoji id
            with open("data/emojis.json","r") as file:
                datacontent = json.load(file)
                for emojiid in datacontent:
                    if key == emojiid["name"]:
                        emoji = emojiid["id"]
                        break
                    else:
                        emoji = ''
                embed.add_field(name = key + " " + emoji, value = val, inline=False)
                    
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Calculator_weapon(bot))