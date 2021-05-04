from discord.ext import commands
import configuration
import traceback
import discord
import difflib
import json
import time
import sys
import os


def get_prefix(bot_, message):
    prefixes = ['i.', 'i!', 'insom!', 'insomniac ']
    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:  # If the message is not in a server.
        return 'i!'  # Only allow this prefix to be used outside of a server.

    with open('guilds.json', 'r') as in_file:
        data = json.load(in_file)

    prefs = data[str(message.guild.id)]['prefix']
    if prefs is not None:
        prefixes.extend(prefs)

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot_, message)


def build_extensions() -> list:
    exts = [cog for cog in os.listdir('cogs/')]
    for pos, val in enumerate(exts):
        if val[-3:] == '.py':
            exts[pos] = val[:-3]
    for ext in exts:
        if ext.startswith('_'):
            exts.remove(ext)
            continue
    return exts


startup_extensions = build_extensions()

bot = commands.Bot(command_prefix=get_prefix, description='Insomniac is a discord bot with a very wide range of commands and features.')

# Embed color values
pingPongRed = 0xC00003
errorRed = 0xff0000
unloadedOrange = 0xf0410f
loadedGreen = 0x3cc80a
mixedBlue = 0x0a55c8
bloodshotRed = 0xb10010


@bot.event
async def on_ready():
    print('--------------------------------')
    print('Username:\t', bot.user.name)
    print('User ID:\t', bot.user.id)
    print('--------------------------------')


@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    ping_embed = discord.Embed(title=':ping_pong: Ping!', color=pingPongRed)
    ping_message = await ctx.send(embed=ping_embed)
    latency = (time.monotonic() - before) * 1000
    pong_embed = discord.Embed(title=f':ping_pong: Pong! `{int(latency)}ms`', color=pingPongRed)
    await ping_message.edit(embed=pong_embed)
    print('ping took {}ms'.format(latency))


@bot.event
async def on_command_error(ctx, error):

    """Error Handler"""

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound, commands.UserInputError)

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except:
            return await ctx.author.send('exception error')

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            return await ctx.send('I could not find that member. Please try again.')

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.message.content)
        embed = discord.Embed(title=':x: **Missing Required Argument**', color=errorRed)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandNotFound):
        unknown_command = ctx.message.content[len(ctx.prefix):].split()[0]
        bot_commands = []
        for c in bot.commands:
            bot_commands.append(c.name)
        embed = discord.Embed(title=f':x: **Command Not Found:** {unknown_command}', color=errorRed)
        matches = difflib.get_close_matches(unknown_command, bot_commands, 10, 0.60)
        if len(matches) == 0:
            embed.add_field(name='**No Close Matches Found**', value='Use `i!help` to check available commands')
        elif len(matches) == 1:
            embed.add_field(name='**Closest Match**', value=matches[0])
        else:
            matches_string = ''
            for m in matches:
                matches_string += f'{m}, '
            embed.add_field(name='**Close Matches:**', value=matches_string[:-2])
        await ctx.send(embed=embed)

    # All other Errors not returned come here... And we can just print the default TraceBack.
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def is_loaded(cog_name: str) -> bool:
    if bot.get_cog(cog_name.capitalize()) is None:
        return False
    else:
        return True


def is_existent(cog_name: str) -> bool:
    cogs = build_extensions()
    if cog_name.lower() in cogs:
        return True
    else:
        return False


@bot.command()
async def load(ctx, extension_name: str = None):
    extension_name = extension_name.lower()

    """Loads an extension."""

    if ctx.message.author.id != configuration.owner_id:
        embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only the bot owner can use this command', color=errorRed)
        await ctx.send(embed=embed)
        print(f'Access was restricted from {ctx.message.author}')
        return

    if extension_name not in build_extensions():
        embed = discord.Embed(title=f':x: **{extension_name.capitalize()} Cog Does Not Exist**', color=errorRed, inline=False)
        await ctx.send(embed=embed)
        print(f'{extension_name} is not an existing cog')
        return

    elif is_loaded(extension_name):
        embed = discord.Embed(title=f':x: **{extension_name.capitalize()} cog:** already loaded', color=errorRed)
        await ctx.send(embed=embed)
        print(f'{extension_name} cog is already loaded')
        return

    try:
        bot.load_extension(f'cogs.{extension_name}')
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return

    embed = discord.Embed(title=f':gear: **{extension_name.capitalize()} cog:** loaded', color=loadedGreen)
    await ctx.send(embed=embed)
    print(f'{extension_name} cog loaded')


@bot.command()
async def unload(ctx, extension_name: str = None):
    extension_name = extension_name.lower()

    """Unloads an extension."""

    if ctx.message.author.id != configuration.owner_id:
        embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only the bot owner can use this command', color=errorRed)
        await ctx.send(embed=embed)
        print(f'Access was restricted from {ctx.message.author}')
        return

    if extension_name == '':
        embed = discord.Embed(title=':x: **Missing argument:** cog name')
        return

    elif extension_name not in build_extensions():
        embed = discord.Embed(title=f':x: **{extension_name.capitalize()} Cog Does Not Exist**', color=errorRed, inline=False)
        await ctx.send(embed=embed)
        print(f'{extension_name} is not an existing cog')
        return

    elif not is_loaded(extension_name):
        embed2 = discord.Embed(title=f':x: **{extension_name.capitalize()} cog:** already unloaded', color=errorRed)
        await ctx.send(embed=embed2)
        print(f'{extension_name} cog is already unloaded')
        return

    bot.unload_extension(f'cogs.{extension_name}')
    embed = discord.Embed(title=f':gear: **{extension_name.capitalize()} cog:** unloaded', color=unloadedOrange)
    await ctx.send(embed=embed)
    print(f'{extension_name} cog unloaded')


@bot.command()
async def reload(ctx, extension_name: str = None):
    extension_name = extension_name.lower()

    """Reloads an extension."""

    if ctx.message.author.id != configuration.owner_id:
        embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only the bot owner can use this command', color=errorRed)
        await ctx.send(embed=embed)
        print(f'Access was restricted from {ctx.message.author}')
        return

    if extension_name == '':
        embed = discord.Embed(title=':x: **Missing argument:** cog name')
        return

    elif extension_name == 'all':
        embed = discord.Embed(title='**Reloaded Cogs**', color=mixedBlue)
        for ext in build_extensions():
            if is_loaded(ext):
                bot.reload_extension(f'cogs.{ext}')
                embed.add_field(name=f'**{ext.capitalize()} cog**', value='reloaded', inline=False)
                print(f'{ext} cog reloaded')
        await ctx.send(embed=embed)
        return

    elif extension_name not in build_extensions():
        embed = discord.Embed(title=f':x: **{extension_name.capitalize()} Cog Does Not Exist**', color=errorRed, inline=False)
        await ctx.send(embed=embed)
        print(f'{extension_name} is not an existing cog')
        return

    elif not is_loaded(extension_name):
        embed2 = discord.Embed(title=f':x: only loaded cogs can be reloaded', color=errorRed)
        await ctx.send(embed=embed2)
        print(f'Can\'t reload {extension_name} cog because it\'s currently unloaded')
        return

    bot.reload_extension(f'cogs.{extension_name}')
    embed = discord.Embed(title=f'**:gear: {extension_name.capitalize()} cog:** reloaded', color=mixedBlue)
    await ctx.send(embed=embed)
    print(f'{extension_name} cog reloaded')


@bot.command()
async def status(ctx, extension_name: str = None):
    extension_name = extension_name.lower()

    """Returns the status of an extension or groups of extensions"""

    if ctx.message.author.id != configuration.owner_id:
        embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only the bot owner can use this command', color=errorRed)
        await ctx.send(embed=embed)
        print(f'Access was restricted from {ctx.message.author}')
        return

    cogs = build_extensions()  # Defines cogs as a list of the extension file names without the .py file type.

    if extension_name == 'all':

        """Returns the status of all the extensions."""

        if len(cogs) == 0:
            embed = discord.Embed(title=':x: **No Cogs Exist to Check**', color=errorRed, inline=False)
            print('No cogs exist to return statuses on')

        else:
            cogs.sort()  # Sorts the list of cog names.
            embed = discord.Embed(title=':gear: **Cog Statuses**', color=mixedBlue, inline=False)
            print(f'{extension_name.capitalize()} Cog Statuses')
            print('----------------------------------------V')
            for c in cogs:  # For every cog.
                if is_loaded(c):
                    embed.add_field(name=f'**{c.capitalize()} cog**', value='loaded', inline=False)
                    print(f'{c.capitalize()} is loaded')
                elif not is_loaded(c):
                    embed.add_field(name=f'**{c.capitalize()} cog**', value=':x: unloaded', inline=False)
                    print(f'{c.capitalize()} is unloaded')
                else:
                    embed.add_field(name='**Error**', value='expected boolean (whether cog is loaded), got different data type', inline=False)

        print('----------------------------------------^\n')
        await ctx.send(embed=embed)

    elif extension_name == 'loaded':

        """Returns a list of all loaded extensions."""

        loaded_cogs = []
        for c in cogs:
            if is_loaded(c):  # If the cog is loaded.
                loaded_cogs.append(c)

        if len(loaded_cogs) == 0:
            embed = discord.Embed(title=':x: **No Loaded Cogs**', color=errorRed, inline=False)
            print('No cogs are loaded to return statuses on')

        else:
            embed = discord.Embed(title=':gear: **Loaded Cogs**', color=loadedGreen, inline=False)
            cogs.sort()  # Sorts the list of cog names.
            print(f'{extension_name.capitalize()} Cog Statuses')
            print('----------------------------------------V')
            for l in loaded_cogs:
                embed.add_field(name=f'**{l.capitalize()} cog**', value='loaded', inline=False)
                print(f'{l.capitalize()} is loaded')
            print('----------------------------------------^')
        await ctx.send(embed=embed)

    elif extension_name == 'unloaded':

        """Returns a list of all unloaded extensions."""

        unloaded_cogs = []
        for c in cogs:
            if not is_loaded(c):  # If the cog is unloaded.
                unloaded_cogs.append(c)

        if len(unloaded_cogs) == 0:
            embed = discord.Embed(title=':x: **No Unloaded Cogs**', color=errorRed, inline=False)
            print('No cogs are unloaded to return statuses on')

        else:
            embed = discord.Embed(title=':gear: **Unloaded Cogs**', color=unloadedOrange, inline=False)
            cogs.sort()  # Sorts the list of cog names.
            print(f'{extension_name.capitalize()} Cog Statuses')
            print('----------------------------------------V')
            for ul in unloaded_cogs:
                embed.add_field(name=f'**{ul.capitalize()} cog**', value='unloaded', inline=False)
                print(f'{ul.capitalize()} is unloaded')
            print('----------------------------------------^')

        await ctx.send(embed=embed)

    else:

        """Returns the status of an extension."""

        if extension_name not in cogs:
            embed = discord.Embed(title=f':x: **{extension_name} Cog Does Not Exist**', color=errorRed, inline=False)
            print(f'{extension_name} is not an existing cog')

        else:
            if is_loaded(extension_name):
                embed = discord.Embed(title=f':gear: **{extension_name.capitalize()} cog:** loaded', color=loadedGreen)
            elif not is_loaded(extension_name):
                embed = discord.Embed(title=f':gear: **{extension_name.capitalize()} cog:** unloaded', color=unloadedOrange)
            else:
                embed = discord.Embed(title='u done messed up, expected boolean (is cog loaded?) but got some other weird messed up data type',
                                      color=errorRed)
            print(f'{extension_name} cog is {"loaded" if is_loaded(extension_name) else "unloaded"}')

        await ctx.send(embed=embed)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(f'cogs.{extension}')
            print(f'loaded {extension} cog')
        except Exception as exception:
            exc = '{}: {}'.format(type(exception).__name__, exception)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(configuration.token, bot=True, reconnect=True)
