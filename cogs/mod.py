import discord
from discord.ext import commands
import configuration
from cogs.config import emojis_maker
import difflib
import string
import json


bloodshotRed = 0xb10010
errorRed = 0xff0000
loadedGreen = 0x3cc80a
alertYellow = 0xffee00

phrase_blocking = None
blocking = False


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        embed = discord.Embed(title='Thanks for adding **Insomniac** to your server: *' + ctx.name + '*',
                              description='This is a little welcome message and a quick guide on how to take advantage of everything that Insomniac has to offer.', colour=bloodshotRed)

        print('joined new guild: ' + ctx.name)
        print('guild id: ' + str(ctx.id))
        print('owner name: ' + self.bot.get_user(ctx.owner_id).name)
        print('owner id: ' + str(ctx.owner_id))
        with open('guilds.json', 'r') as in_file:
            data = json.load(in_file)
        if str(ctx.id) not in data:
            data[str(ctx.id)] = {'name': ctx.name, 'owner_id': ctx.owner_id, 'prefix': None, 'moderators': [ctx.owner_id]}
            with open('guilds.json', 'w') as out_file:
                json.dump(data, out_file)
        await self.bot.get_user(ctx.owner_id).send(embed=embed)

    #@commands.Cog.listener()
    #async def on_member_join(self, member):
    #    with open('guilds.json', 'r') as in_file:
    #        data = json.load(in_file)
    #    owner = self.bot.get_user(data[member.guild.id]['owner_id'])
    #    embed = discord.Embed(title=f'<@{owner.id}> joined {self.bot.get_guild(member.guild.id)}', color=bloodshotRed)
    #    embed.add_field(name='User Name', value=member.display_name)  # self.bot.get_user(member)
    #    embed.add_field(name='User ID', value=member.id)
    #    # embed.set_image(url=member.avatar_url)
    #    await owner.send(embed=embed)

    @commands.command()
    async def role(self, ctx, mention: discord.Member = None, *role_name):

        """Changes the role by mention or by author."""

        r_name = ''
        for word in role_name:
            r_name += word.capitalize() + ' '
        r_name = r_name[:-1]
        guild = ctx.guild
        admin = discord.utils.get(guild.roles, name='Admin')
        if admin not in ctx.message.author.roles:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only an admin can use this command', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return

        r_list = guild.roles  # List of role objects
        role_names = []  # Empty list for role names which are strings
        for ro in r_list:  # For every role object in the list of role objects
            role_names.append(ro.name)  # Appends the name (string) of the role object to the list of role names

        if r_name not in role_names:  # Checks if the role doesn't already exist and creates it if it doesn't
            await guild.create_role(name=r_name)
            print(f'Creating role "{r_name}"')
        else:
            print(f'Role "{r_name}" already exists')

        assigning_role = discord.utils.get(guild.roles, name=r_name)

        if assigning_role in mention.roles:  # If the role does exist, it checks if the person already has the role
            embed = discord.Embed(title=f':x: {mention.display_name} already has the role "{r_name}"', color=errorRed)
            await ctx.send(embed=embed)
            print(f'{mention.display_name} already has the role "{r_name}"')
            return

        await mention.add_roles(assigning_role)  # Once everything has been handled, it adds the role to the member
        await ctx.send(f'Added role "{r_name}" to {mention.name}')  # Sends message of task to channel
        print(f'Added role "{r_name}" to {mention.name}')  # Prints task to console

    @commands.command()
    async def quiet(self, ctx, *args):
        global phrase_blocking
        global blocking
        if args[0].lower() == 'stop':
            phrase_blocking = False
            blocking = None
            return
        phrase = ''
        for word in args:
            phrase += word.lower() + ' '
        phrase_blocking = phrase[:-1]
        blocking = True

    @commands.Cog.listener()
    async def on_message(self, message):
        global phrase_blocking
        global blocking
        if blocking and (difflib.get_close_matches(phrase_blocking.lower(), message.content.lower().split(), cutoff=0.5) != []) and '!quiet ' not in message.content.lower():
            await message.delete()

    @commands.command()
    async def count(self, ctx, emoji: str, channel: str = None):
        if channel is None:
            channel = ctx.message.channel
        else:
            channel = discord.utils.get(self.bot.get_all_channels(), guild=ctx.message.guild, name=channel)
        winner = None
        async for message in channel.history(limit=999):
            for reaction in message.reactions:
                if 'knightro' in str(reaction).lower():
                    try:
                        if reaction.count > winner[1]:
                            winner = (message, reaction.count)
                            print('new winner')
                    except (AttributeError, TypeError):
                        winner = (message, reaction.count)
                        print('setting first winner')
        await ctx.send(f'`{winner[0].content}` won by {winner[1]}')


def setup(bot):
    bot.add_cog(Mod(bot))
