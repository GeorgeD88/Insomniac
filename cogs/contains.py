import discord
from discord.ext import commands
import configuration
from time import sleep
from random import choice
import requests
from PIL import Image
import os


errorRed = 0xff0000
seeking = None


class Contains(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # TODO: Add any emoji
    async def nope(self, ctx, contains=None):
        global seeking
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command pussyass bitch', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        if contains is None:
            print('empty argument')
            seeking = None
            return
        seeking = contains.lower()

    @commands.Cog.listener()
    async def on_message(self, message):
        if seeking is not None and seeking in message.content.lower() and message.content.lower() != 'i!nope ' + str(seeking):
            await message.delete()
            await message.channel.send('no:heart:')
            print(f'noped {seeking} in {str(message.channel)}: {message.content}')


def setup(bot):
    bot.add_cog(Contains(bot))
