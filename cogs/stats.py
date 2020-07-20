import discord
from discord.ext import commands
import random
import json


pinkishPurple = 0xd714f5


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, title: str, *options_split: str):  # TODO: Make title multiword
        print(options_split)
        str_arg = ''
        for opt in options_split:
            str_arg += opt + ' '
        str_arg = str_arg[:-1]
        options = str_arg.split(', ')

        with open('guilds.json', 'r') as in_file:
            emojis = json.load(in_file)[str(ctx.guild.id)]['poll_emojis']
        embed = discord.Embed(title=title, color=pinkishPurple)
        for pos, opt in list(enumerate(options)):
            print(emojis)
            emoji = emojis.pop(random.randint(0, len(emojis)))
            embed.add_field(name=opt, value=emoji, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
