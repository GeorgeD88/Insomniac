import discord
from discord.ext import commands
import configuration
import win32com.client
import os


ignoring = None
hard = False

errorRed = 0xff0000


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def toggle(self, ctx, *words):  # TODO: Find a better name
        toggled = ''
        last_upper = True
        plaintext = ''
        for word in words:
            plaintext += word + ' '
        plaintext = plaintext[:-1]
        for ch in list(plaintext.lower()):
            if ch.isalpha():
                toggled += ch if last_upper else ch.upper()
                last_upper = not last_upper
            else:
                toggled += ch
        await ctx.send(toggled)

    @commands.command()
    async def ignore(self, ctx, mention, is_hard: bool = False):
        global ignoring
        global hard
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command pussyass bitch', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        if mention == 'stop':
            ignoring = None
            hard = False
            print('ending silent treatment')
            return
        else:
            ignoring = mention[3:-1]  # Saves the ID from the mention
            hard = is_hard
            print(('ignoring ' + mention) if not is_hard else ('hard ignoring ' + mention))

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) == ignoring:
            if hard:
                await message.delete()
            await message.channel.send('ya\'ll hear sumn?')
            print(f'{ignoring} in {message.channel}: {message.content}')

    @commands.command()
    async def homies(self, ctx, *args):
        hate = ''
        # TODO: If the line is too long, move text up and add extra line
        for word in args:
            hate += word + ' '
        hate = hate[:-1]

        ps = win32com.client.Dispatch("Photoshop.Application")
        ps.Open(r"C:\Users\Georg\Documents\homies.psd")
        layers = ps.Application.ActiveDocument

        top = layers.ArtLayers['Top Text']
        top_text = top.TextItem
        top_text.contents = 'FUCK ' + hate
        bottom = layers.ArtLayers['Bottom Text']
        bottom_text = bottom.TextItem
        bottom_text.contents = 'HATE ' + hate

        options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        options.Format = 13  # PNG Format
        options.PNG8 = False  # Sets it to PNG-24 bit
        pngfile = r"C:\Users\Georg\Documents\homies.png"
        layers.Export(ExportIn=pngfile, ExportAs=2, Options=options)
        file = discord.File(pngfile, filename='homies.png')
        await ctx.channel.send("", file=file)

    @commands.command()
    async def chickenwing(self, ctx):
        await ctx.send('chicken :rooster: wing :poultry_leg: chicken :rooster: wing :poultry_leg: hotdog :hotdog: and bologna :sparkles: chicken :chicken: and macaroni :spaghetti: chillin :cold_face: with my :kissing_heart: homies :women_with_bunny_ears_partying:')


def setup(bot):
    bot.add_cog(Fun(bot))
