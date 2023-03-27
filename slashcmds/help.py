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
    async def help(self, interaction: discord.Interaction, command: Optional[Literal['all','link', 'authkey', 'notifications','abbys','characters','pity','wish_history','resources','diary','daily','profile','auto','calculator_weapon','calculator_character']] = None):
        if command is None:
            embed = discord.Embed(title="GenshinStalker Helper",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='', value ='<@1064985978651017318> is a discord bot written by <@333670274216099850>!', inline=False)
            embed.add_field(name='Want to get all avaliable commands?', value ='Try using `/help command:all`', inline=False)
            embed.add_field(name='Want to learn more about a specific command?', value ='Try specifying the command name on the `help` command: `/help command:_`', inline=False)
            embed.add_field(name='Want to invite the bot to your server?', value ='Try using this: https://discord.com/api/oauth2/authorize?client_id=1064985978651017318&permissions=534723950656&scope=bot', inline=False)
            embed.add_field(name='Why do I have to link authkey', value ="Authkey allows me to get your wish history and is absolutely safe to share. For more information read `/help commad:authkey`", inline=False)
            embed.add_field(name='Why do I have to link cookies', value ="Cookies allows me to get your hoyolab stats and are **NOT SAFE TO SHARE** (I can probably steal your account but dunno how anyway). Before linking your cookies **PLEASE READ** `/help commad:cookies` for more information ", inline=False)
            embed.add_field(name='See a bug?', value ="Feel free to contact me, I'll be really thankful! <@333670274216099850>", inline=False)
            embed.add_field(name='Want to help me with this project?', value ="If you want to help me with this project and you have a base knowledge of using git and coding in python, then feel free to dm me :)", inline=False)

            await interaction.response.send_message(embed = embed)

        elif command == 'all':
            embed = discord.Embed(title="List of all avaliable commands",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='', value ='`/link` Links your hoyolab browser cookies', inline=False)
            embed.add_field(name='', value ='`/authkey` Links your genshin authkey', inline=False)
            embed.add_field(name='', value ='`/pity` Shows your current pity', inline=False)
            embed.add_field(name='', value ='`/wish_history` Shows your wish history', inline=False)
            embed.add_field(name='', value ='`/daily` Reedems your daily check in from hoyolab', inline=False)
            embed.add_field(name='', value ='`/characters` Shows your owned characters', inline=False)
            embed.add_field(name='', value ='`/profile` Shows your genshin stats', inline=False)
            embed.add_field(name='', value ='`/abbys` Shows your previous abbys stats', inline=False)
            embed.add_field(name='', value ='`/notifications` Enables *ping* notifications if your resing/realm currency is full', inline=False)
            embed.add_field(name='', value ='`/diary` Shows primogems earned this month', inline=False)
            embed.add_field(name='', value ='`/calculator_character` Calculates materials required to build a character', inline=False)
            embed.add_field(name='', value ='`/calculator_weapon` Calculates materials required to ascend a weapon', inline=False)
            embed.add_field(name='', value ='`/auto` Automatically claims your daily from hoyolab', inline=False)
            embed.add_field(name='', value ='`/resources` Shows your current resin and realm currency', inline=False)
            embed.add_field(name='If you want to get more informations about a specific command type `/help command:___`', value ='', inline=False)
            await interaction.response.send_message(embed=embed)
    
        elif command == 'link':
            embed = discord.Embed(title="READ THIS BEFORE LINKING YOUR COOKIES!!!",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What are cookies?', value ='Cookies are the default form of authentication over the majority of Mihoyo APIs. These are used in web events and hoyolab utilities such as the Battle Chronicle. The cookies used in these APIs are the same as the ones you use to log in to your hoyolab account', inline=False)
            embed.add_field(name="What does it mean?", value ="I can probably steal your account if you link them (I don't know how anyway), so if you dont trust me **PLEASE DONT LINK YOUR COOKIES**", inline=False)
            embed.add_field(name='Can I still use a bot without linking my cookies?', value ="Of course you can! You can still use commands such as `/pity` `/calculator` `/wish_history` etc. Unfortunately some commands requires your cookies so they will be locked", inline=False)
            embed.add_field(name='What commands are *locked* without providing cookies?', value ="`/diary` `/notifications` `/abbys` `/resources` `/profile` `/characters` `/daily`", inline=False)
            embed.add_field(name="Ok I've read that so how can I link my cookies?", value ="", inline=False)
            embed.add_field(name="", value ="**1.** Go to https://www.hoyolab.com.", inline=False)
            embed.add_field(name="", value ="**2.** Login to your account.", inline=False)
            embed.add_field(name="", value ="**3.** Press F12 to open Inspect Mode (ie. Developer Tools).", inline=False)
            embed.add_field(name="", value ="**4.** Go to Application, Cookies, https://www.hoyolab.com.", inline=False)
            embed.add_field(name="", value ="**5.** Copy ltuid and ltoken.", inline=False)
            embed.add_field(name="", value ="**6.** Type `/link` and enter what you've copied!", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'authkey':
            embed = discord.Embed(title="Authkey Helper",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What is authkey?', value ='Authkeys are an alternative authentication.', inline=False)
            embed.add_field(name="Are they safe to share?", value ="Authkeys last only 24 hours, and it's impossible to do any write operations with them. That means authkeys, unlike cookies, **are absolutely safe to share.**", inline=False)
            embed.add_field(name='Can I still use a bot without linking my authkey?', value ="Of course you can! You can still use commands such as `/banner` `/domains` `/calculator` etc. Unfortunately some commands requires your authkey so they will be *locked*", inline=False)
            embed.add_field(name='What commands are *locked* without providing authkey?', value ="`/pity` `/wish_history`", inline=False)
            embed.add_field(name="How can I link my authkey?", value ="", inline=False)
            embed.add_field(name="", value ="**1.** Press START on your keyboard, then search for Powershell", inline=False)
            embed.add_field(name="", value ="**2.** Click Windows Powershell, then copy & paste the script below to the Powershell, then press ENTER (only when 'Press Enter to continue...' message is not showing yet)", inline=False)
            embed.add_field(name="", value ="`Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://gist.githubusercontent.com/MadeBaruna/bf36bad751dc9221067ca1e31ab08255/raw/cb73a9f46f08fad6f27581ebb1a6249ba086af13/read.ps1'))`", inline=False)
            embed.add_field(name="", value ="**3.** Open Genshin Impact in this PC", inline=False)
            embed.add_field(name="", value ="**4.** Then open the wish history in the game and wait it to load", inline=False)
            embed.add_field(name="", value ="**5.** Click the table, then press CTRL+A then CTRL+C", inline=False)
            embed.add_field(name="", value ="**6.** Alt+Tab to the powershell, then press ENTER, the link will be copied to your clipboard", inline=False)
            embed.add_field(name="", value ="**7.** Type `/authkey` and paste the text to the textbox", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'notifications':
            embed = discord.Embed(title="Notifications",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It pings you whenever your resin or realm curresncy is full', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'diary':
            embed = discord.Embed(title="Diary",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows how many primogems you farmed this month', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'daily':
            embed = discord.Embed(title="Daily",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It claims for you your daily rewards from hoyolab daily check-in', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'profile':
            embed = discord.Embed(title="Profile",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows your account stats e.g: achievements, days spent in genshin, spiral abbys and more!', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'characters':
            embed = discord.Embed(title="Characters",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows informations about your owned characters', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'wish_history':
            embed = discord.Embed(title="Wish History",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows your wish history', inline=False)
            embed.add_field(name="I summoned 5 star an hour ago why I don't see it on the list?", value ='You have to update your authkey everytime you make a wish. Sadly authkeys are not updating automatically :( For more information type `/help:authkey`', inline=False)
            embed.add_field(name='', value ="Note that you have to set your authkey first. If you didn't, please type `/help command:authkey` and then `/authkey`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'pity':
            embed = discord.Embed(title="Pity",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows your pity on every banner avaliable', inline=False)
            embed.add_field(name="I summoned 5 star an hour ago why my pity counter is not updated?", value ='You have to update your authkey everytime you make a wish. Sadly authkeys are not updating automatically :( For more information type `/help:authkey`', inline=False)
            embed.add_field(name='', value ="Note that you have to set your authkey first. If you didn't, please type `/help command:authkey` and then `/authkey`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'abbys':
            embed = discord.Embed(title="Abbys",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows your previous abbys stats', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)
        
        elif command == 'resources':
            embed = discord.Embed(title="Resources",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It shows your current resin, realm currency and expeditions capacity', inline=False)
            embed.add_field(name='', value ="Note that you have to set your cookies first. If you didn't, please type `/help command:link` and then `/link`", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'calculator_character':
            embed = discord.Embed(title="Calculator character",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It calculates materials required to build a character', inline=False)
            embed.add_field(name='What should I type in *current* and *target* fields', value ="The *current* field is the current level of your character. The *target* field is the target level you want your character to ascend", inline=False)
            embed.add_field(name="Why can't I choose a character that was leaked 0.5262ms ago?", value="Give me a time to update characters. I'm developing this bot alone and I have a private life as well :). Feel free to contact me if you don't see a character that was released more than a week ago", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'calculator_weapon':
            embed = discord.Embed(title="Resources",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It calculates materials required to ascend a weapon', inline=False)
            embed.add_field(name='What should I type in *current* and *target* fields', value ="The *current* field is the current level of your weapon. The *target* field is the target level you want your weapon to ascend", inline=False)
            embed.add_field(name="Why can't I choose a character that was leaked 0.5262ms ago?", value="Give me a time to update weapons. I'm developing this bot alone and I have a private life as well :). Feel free to contact me if you don't see a weapon that was released more than a week ago", inline=False)
            await interaction.response.send_message(embed=embed)

        elif command == 'auto':
            embed = discord.Embed(title="Auto",color=discord.Color.from_rgb(219, 42, 166))
            embed.add_field(name='What does this command do?', value ='It automatically do something for you based on your selected option :)', inline=False)
            embed.add_field(name='What options are available?', value ="For now only the `daily` option", inline=False)
            embed.add_field(name='What does daily option do?', value ="It redeems your daily rewards from hoyolab every 24 hours, so you don't have to type `/daily` everyday", inline=False)
            embed.add_field(name='Can I unsign from it?', value ="Of course! Just type `/auto` and choose the option that you want to unsign from", inline=False)
            await interaction.response.send_message(embed=embed)
        
        else:
            await interaction.response.send_message(f'You did not select any commands.')
        

async def setup(bot):
    await bot.add_cog(Help(bot))