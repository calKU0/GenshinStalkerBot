import discord
import json
from replit import Database
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional

with open("config.json") as config:
    content = json.load(config)
    DATABASE = content["DATABASE"]
    db = Database(db_url=DATABASE)

class Help(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot   

    @app_commands.command(name="help", description="Helps you :)")
    async def help(self, interaction: discord.Interaction, commands: Optional[Literal['link', 'authkey', 'notifications']] = None):
        if commands is None:
            embed = discord.Embed(title="GenshinStalker Helper",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='', value ='<@1064985978651017318> is a discord bot written by calKU!', inline=False)
            embed.add_field(name='Want to get all avaliable commands?', value ='Try using `/help command:all`', inline=False)
            embed.add_field(name='Want to learn more about a specific command?', value ='Try specifying the command name on the `help` command: `/help command:_`', inline=False)
            embed.add_field(name='Want to invite the bot to your server?', value ='Try using this "bedzie tu potem inv link"', inline=False)
            embed.add_field(name='Why do I have to link authkey', value ="Authkey allows me to get your wish history and is absolutely safe to share. For more information read `/help commad:authkey`", inline=False)
            embed.add_field(name='Why do I have to link cookies', value ="Cookies allows me to get your hoyolab stats and are **NOT SAFE TO SHARE** (I can probably steal your account but dunno how anyway). Before linking your cookies **PLEASE READ** `/help commad:cookies` for more information ", inline=False)
            await interaction.response.send_message(embed = embed)
        else:
            await interaction.response.send_message(f'You did not select any commands.')

async def setup(bot):
    await bot.add_cog(Help(bot))
