import discord
from discord.ext import commands


class Color(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hexcolor(self, ctx, ):
        pass


def setup(bot):
    bot.add_cog(Color(bot))
