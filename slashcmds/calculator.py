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
    client.set_cookies(ltuid=content["GENSHIN_COOKIE1"], ltoken=content["GENSHIN_COOKIE2"])
    
async def character_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    characters = ["Traveler", "Amber", "Kaeya", "Lisa", "Jean", "Diluc", "Venti", "Razor", "Keqing", "Qiqi", "Mona", "Xiangling", "Klee", "Tartaglia", "Zhongli", "Diona", "Xinyan", "Albedo", "Ganyu", "Hu Tao", "Eula", "Yanfei", "Sayu", "Raiden Shogun", "Kokomi", "Sara", "Thoma", "Aloy","Nahida","Dehya","Layla","Candace","Tighnari","Collei","Yae Miko","Yelan"]
    choices = [
        app_commands.Choice(name=character, value=character)
        for character in characters if current.lower() in character.lower()
    ]
    return choices[:25]

class Calculator(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   


    @app_commands.command(name="calcualtor",description="siema")
    @app_commands.autocomplete(character=character_autocomplete)
    async def calculator(self,interaction: discord.Interaction, character: str):
        with open("characters.json") as config:
            content = json.load(config)
            characterid = content[character]

        builder = client.calculator()
        builder.set_character(characterid, current=1, target=90)

        cost = await builder.calculate()
        
        print(cost)


        await interaction.response.send_message(f'character {character}')


async def setup(bot):
    await bot.add_cog(Calculator(bot))