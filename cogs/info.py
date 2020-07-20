import discord
from discord.ext import commands
import json

bloodshotRed = 0xb10010
#errorRed = 0xff00000
#loadedGreen = 0x3cc80a


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, *, mention: discord.Member = None):
    
        """Returns a user's info by mention or by author."""

        user = ctx.message.author if mention is None else mention
        user_id = user.id

        embed = discord.Embed(title=f'**{user}\'s Info**', color=user.top_role.color)
        embed.set_image(url=user.avatar_url)
        embed.add_field(name='**User Name**', value=user, inline=True)
        embed.add_field(name='**User ID**', value=user_id, inline=True)
        embed.add_field(name='**Joined On**', value=user.joined_at.strftime('%m/%d/%y'), inline=True)
        embed.add_field(name='**Account Created**', value=user.created_at.strftime('%m/%d/%y'), inline=True)
        embed.add_field(name='**Status**', value=str(user.status).capitalize(), inline=True)
        embed.add_field(name='**Highest Role**', value=user.top_role, inline=True)
        await ctx.send(embed=embed)
        print('Returned info on user: ' + str(user))

    @commands.command()
    async def avatar(self, ctx, *, mention: discord.Member = None):

        """Returns a user's avatar by mention or by author."""

        user = ctx.message.author if mention is None else mention

        embed = discord.Embed(title=f'{user}\'s Profile Pic', color=user.top_role.color)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def details(self, ctx):
        guild = ctx.guild
        app_info = await self.bot.application_info()

        embed = discord.Embed(title='**Insomniac** Bot Details', color=bloodshotRed)
        embed.set_image(url=self.bot.user.avatar_url)
        embed.add_field(name='**Name**', value='Insomniac')
        embed.add_field(name='**ID**', value=app_info.id)
        embed.add_field(name='**Bot Creator**', value=self.bot.get_user(app_info.owner.id))
        embed.add_field(name='**Creator ID**', value=app_info.owner.id)
        embed.add_field(name='**Creator Status**', value=str(guild.get_member(app_info.owner.id).status).capitalize())
        #embed.add_field(name='**Server Name**', value=ctx.message.guild)
        #embed.add_field(name='**Server ID**', value=ctx.message.guild.id)
        await ctx.send(embed=embed)

    @commands.command()
    async def settings(self, ctx):
        app_info = await self.bot.application_info()
        guild = ctx.guild

        embed = discord.Embed(title='**Insomniac** Settings', color=bloodshotRed)
        embed.add_field(name='**Highest Role**', value=guild.get_member(app_info.id).top_role)
        embed.add_field(name='**Default Prefixes**', value='i., i!, insom!, insomniac ')
        with open('guilds.json', 'r') as in_file:
            data = json.load(in_file)
        embed.add_field(name='**Server Prefixes**', value=data[str(ctx.message.guild.id)]['prefix'])
        await ctx.send(embed=embed)

    @commands.command()
    async def guild_id(self, ctx):
        await ctx.send(ctx.guild.id)


def setup(bot):
    bot.add_cog(Info(bot))
