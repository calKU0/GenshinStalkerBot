import discord
from discord import app_commands
import json


async def character_autocomplete(interaction: discord.Interaction,
    current: str,) -> list[app_commands.Choice[str]]:
    with open("data/characters.json","r") as file:
        content = json.load(file)
        choices = [
            app_commands.Choice(name=key, value=key)
            for key in content.keys() if current.lower() in key.lower()
            ]
    return choices[:25]
    

async def weapon_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        with open("data/weapons.json","r") as file:
            content = json.load(file)
            choices = [
                app_commands.Choice(name=key, value=val)
                for key,val in content.items() if current.lower() in key.lower()
            ]
        return choices[:25]