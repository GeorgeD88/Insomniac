import discord
from discord.ext import commands
import configuration
from time import sleep
from random import choice
import requests
from PIL import Image
import os


downing = None


class Down(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # TODO: Add any emoji
    async def down(self, ctx, mention: discord.Member = None):
        global downing
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command pussyass bitch', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        if mention is None:
            print('empty mention')
            downing = None
            return
        downing = mention.id

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == downing:
            await message.add_reaction('downvote:713867711293292555')
            print('downvoted in ' + str(message.channel))


def setup(bot):
    bot.add_cog(Down(bot))
