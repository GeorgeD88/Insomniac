import discord
from discord.ext import commands
import requests
import json
import ast

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'SOAPAction': 'http://www.corp.net/some/path/CustMsagDown.Check',
    'Content-type': 'text/xml'
}


class Urban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *args):
        search = ''
        for word in args:
            search += word.capitalize() + ' '
        search = search[:-1]
        try:
            req = requests.get(f'https://api.urbandictionary.com/v0/define?term={search}', headers=headers)
        except Exception as ex:
            return

        content = ast.literal_eval(req.content.decode('utf-8'))

        try:
            definition = content['list'][0]['definition']
        except IndexError:
            await ctx.send('No definitions for ' + search)
            return

        if len(definition) > 1024:
            definition = definition[:1021] + '...'

        embed = discord.Embed(title='Definition of ' + search, color=0x134FE6)
        embed.add_field(name=search, value=definition)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Urban(bot))
