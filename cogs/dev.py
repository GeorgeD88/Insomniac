import discord
from discord.ext import commands
import configuration
from time import sleep
from random import choice
import requests
from PIL import Image
import os


errorRed = 0xff0000


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def message(self, ctx, recipient, *args):
        if not args:  # If args doesn't contain anything.
            embed = discord.Embed(title=':x: Missing Argument', color=0xC40000)
            embed.add_field(name='yuh', value='ooh')
            await ctx.send(embed=embed)
        else:
            to_send = ''
            for arg in args:
                to_send += f'{arg} '
            recipient_id = ctx.message.mentions[0].id
            await self.bot.get_user(recipient_id).send(to_send)

    @commands.command()  # TODO: MAKE DECORATOR TO DO OWNER CHECKING
    async def guilds(self, ctx):
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        guilds = self.bot.guilds
        output = ''
        for g in guilds:
            output += g.name + '\n'
        await ctx.send(output[:-1])


def setup(bot):
    bot.add_cog(Dev(bot))
