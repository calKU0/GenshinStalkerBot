import discord
from discord import ui
from discord.ui import View
from typing import List, Optional

class ButtonMenu(View):
    def __init__(self, pages: list, timeout: float) -> None:
        super().__init__(timeout=timeout)
        self.current_page = 0
        self.pages = pages
        self.length = len(self.pages)-1
    
    async def update(self,page:int):
        self.current_page = page
        if page == 0:
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[-1].disabled = False
            self.children[-2].disabled = False
        elif page==self.length:
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[-1].disabled = True
            self.children[-2].disabled = True
        else:
            for i in self.children: i.disabled = False

    async def getPage(self,page):
        if isinstance(page,str):
            return page,[],[]
        elif isinstance(page,discord.Embed):
            return None,[page],[]
        elif isinstance(page,discord.File):
            return None, [], [page]
        elif isinstance(page,List):
            if all(isinstance(x,discord.Embed) for x in page):
                return None,page,[]
            elif all(isinstance(x,discord.File) for x in page):
                return None,[],page
            else:
                raise TypeError("Can't have alternative files and embeds")
        else:
            #error
            pass

    async def showPage(self,page:int, interaction:discord.Interaction):
        await self.update(page)
        content, embeds, files = await self.getPage(self.pages[page])

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            attachments=files or [],
            view=self
        )

    @ui.button(emoji = "<:518652l:1065414396706304060>", style = discord.ButtonStyle.blurple)
    async def first_page(self,interaction,button):
        await self.showPage(0,interaction)

    @ui.button(emoji = "<:4838appdirectorylarrowblokw:1065410232295104593>", style = discord.ButtonStyle.green)
    async def before_page(self,interaction,button):
        await self.showPage(self.current_page-1,interaction)

    @ui.button(emoji = "<:6405appdirectoryrarrowblokw:1065410208517603349>", style = discord.ButtonStyle.green)
    async def next_page(self,interaction,button):
        await self.showPage(self.current_page+1,interaction)

    @ui.button(emoji = "<:518652r:1065414566147788960>", style = discord.ButtonStyle.blurple)
    async def last_page(self,interaction,button):
        await self.showPage(self.length,interaction)


