import discord
from discord.ext import commands
import configuration
from time import sleep
from random import choice
import requests
from PIL import Image
import os


bobbing = None


class Sponge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bob(self, ctx, mention: discord.Member = None):
        global bobbing
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command pussyass bitch', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        if mention is None:
            print('empty mention')
            bobbing = None
            return
        bobbing = mention.id

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == bobbing:
            await message.delete()

            toggled = ''
            last_upper = True

            for ch in list(message.content.lower()):
                if ch.isalpha():
                    toggled += ch if last_upper else ch.upper()
                    last_upper = not last_upper
                else:
                    toggled += ch
            await message.channel.send(f'{message.author}: {toggled}')
            print('heard spongebob in ' + str(message.channel))


def setup(bot):
    bot.add_cog(Sponge(bot))
