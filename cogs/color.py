import discord
from discord.ext import commands


class Color(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hexcolor(self, ctx, hex_code):
        if not hex_code.isalnum():  # checks if it contains letters and numbers only
            embed = discord.Embed(title=':X: **Error:** Hexcode must only contain letters and numbers and be exactly 6 characters long', color=0xff0000)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=hex_code.upper(), color=int(hex_code, 16))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Color(bot))
