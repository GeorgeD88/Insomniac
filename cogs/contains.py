import discord
from discord.ext import commands
import configuration
from time import sleep
from random import choice
import requests
from PIL import Image
import os


seeking = None


class Down(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # TODO: Add any emoji
    async def check(self, ctx, contains):
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
        if seeking in message.content.lower() and seeking is not None:
            await message.delete()
            await message.channel.send('no:heart:')
            print(f'avoided {seeking} in {str(message.channel)}')


def setup(bot):
    bot.add_cog(Down(bot))
