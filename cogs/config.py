import discord
from discord.ext import commands
import json
import configuration


bloodshotRed = 0xb10010
errorRed = 0xff0000
loadedGreen = 0x3cc80a
alertYellow = 0xffee00


def emojis_maker(ctx, emoji_list: list):  # TODO: Simplify arguments to default emojis or not.
    if len(emoji_list) == 0:
        save_emojis = [':octopus:', ':dog:', ':cat:', ':sun_with_face:', ':tennis:', ':full_moon_with_face:', ':soccer:',
                  ':volleyball:', 'ping_pong:', ':basketball:', ':football:', ':baseball:', ':red_car:',
                  ':telephone_receiver:', ':floppy_disk:', ':money_with_wings:' ':dollar:', ':warning:',
                  ':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:',
                  ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:',
                  ':regional_indicator_g:', ':regional_indicator_h:', ':regional_indicator_i:',
                  ':regional_indicator_j:', ':regional_indicator_k:', ':regional_indicator_l:',
                  ':regional_indicator_m:', ':regional_indicator_n:', ':regional_indicator_o:',
                  ':regional_indicator_p:', ':regional_indicator_q:', ':regional_indicator_r:',
                  ':regional_indicator_s:', ':regional_indicator_t:', ':regional_indicator_u:',
                  ':regional_indicator_v:', ':regional_indicator_w:', ':regional_indicator_x:',
                  ':regional_indicator_y:', ':regional_indicator_z:', ':radioactive:', ':arrow_forward:',
                  ':arrow_backward:', ':pause_button:', 'evergreen_tree', ':flag_us:', ':link:', ':musical_score:']
        default = True
    else:
        save_emojis = emoji_list
        default = False
    return save_emojis, f'Set poll emojis to {"default" if default else "desired"} list'


class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix: str):
        print(ctx.guild.owner.id)
        with open('guilds.json', 'r') as in_file:
            mods = json.load(in_file)[str(ctx.guild.id)]['moderators']
        if ctx.message.author.id not in mods:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only a moderator can use this command',
                                  coqlor=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return
        with open('guilds.json', 'r') as in_file:
            data = json.load(in_file)
        data[str(ctx.message.guild.id)]['settings']['prefix'] = prefix
        print('prefix set to ' + prefix)
        with open('guilds.json', 'w') as out_file:
            json.dump(data, out_file)
        embed = discord.Embed(title=f'Server prefix set to `{prefix}`', color=loadedGreen)
        await ctx.send(embed=embed)

    @commands.command()
    async def moderator(self, ctx, mention: discord.Member = None, remove: str = False):
        with open('guilds.json', 'r') as in_file:
            owner_id = json.load(in_file)[str(ctx.guild.id)]['owner_id']
        if ctx.message.author.id != owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only the server owner can use this command',
                                  color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted  from {ctx.message.author}')
            return
        user = ctx.message.author if mention is None else mention
        with open('guilds.json', 'r') as in_file:
            data = json.load(in_file)
        if not remove:
            if user.id == data[str(ctx.guild.id)]['owner_id']:
                embed = discord.Embed(title=f'**Server Owner {user}** is Always a Moderator', color=errorRed)
                print(f'attempted to add server owner {user} to moderators')
            elif user.id in data[str(ctx.guild.id)]['moderators']:
                embed = discord.Embed(title=f'**{user}** is Already a Moderator', color=errorRed)
                print(f'{user} is already a moderator')
            else:
                data[str(ctx.guild.id)]['moderators'].append(user.id)
                embed = discord.Embed(title=f'**{user}** Set to Moderator', color=alertYellow)
                print(str(user) + ' set to moderator')
                with open('guilds.json', 'w') as out_file:
                    json.dump(data, out_file)
        else:
            if user.id not in data[str(ctx.guild.id)]['moderators']:
                embed = discord.Embed(title=f'**{user}** is not a Moderator', color=errorRed)
                print(f'attempted to remove non-moderator {user} from moderators')
            elif user.id == data[str(ctx.guild.id)]['owner_id']:
                embed = discord.Embed(title=f'**Server Owner {user}** Cannot be Removed from Moderators', color=errorRed)
                print(f'attempted to remove server owner {user} from moderators')
            else:
                data[str(ctx.guild.id)]['moderators'].remove(user.id)
                embed = discord.Embed(title=f'**{user}** Removed from Moderators', color=alertYellow)
                print(str(user) + ' removed from moderators')
                with open('guilds.json', 'w') as out_file:
                    json.dump(data, out_file)
        await ctx.send(embed=embed)

    @commands.command()
    async def poll_emojis(self, ctx, *emojis: list):
        #if len(emojis) == 0:
        #    emojis = [':octopus:', ':dog:', ':cat:', ':sun_with_face:', ':tennis:', ':full_moon_with_face:', ':soccer:',
        #              ':volleyball:', 'ping_pong:', ':basketball:', ':football:', ':baseball:', ':red_car:',
        #              ':telephone_receiver:', ':floppy_disk:', ':money_with_wings:' ':dollar:', ':warning:',
        #              ':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:',
        #              ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:',
        #              ':regional_indicator_g:', ':regional_indicator_h:', ':regional_indicator_i:',
        #              ':regional_indicator_j:', ':regional_indicator_k:', ':regional_indicator_l:',
        #              ':regional_indicator_m:', ':regional_indicator_n:', ':regional_indicator_o:',
        #              ':regional_indicator_p:', ':regional_indicator_q:', ':regional_indicator_r:',
        #              ':regional_indicator_s:', ':regional_indicator_t:', ':regional_indicator_u:',
        #              ':regional_indicator_v:', ':regional_indicator_w:', ':regional_indicator_x:',
        #              ':regional_indicator_y:', ':regional_indicator_z:', ':radioactive:', ':arrow_forward:',
        #              ':arrow_backward:', ':pause_button:', 'evergreen_tree', ':flag_us:', ':link:', ':musical_score:']
        #    print('set poll emojis to default list')
        #    await ctx.send('Set poll emojis to default list')
        #else:
        #    print('set poll emojis to argument list')
        #    await ctx.send('Set poll emojis to desired list')
        #with open('guilds.json', 'r') as in_file:
        #    data = json.load(in_file)
        #data[str(ctx.guild.id)]['poll_emojis'] = emojis
        #with open('guilds.json', 'w') as out_file:
        #    json.dump(data, out_file)

        save_emojis, message = emojis_maker(ctx, list(emojis))
        with open('guilds.json', 'r') as in_file:
            data = json.load(in_file)
        data[str(ctx.guild.id)]['poll_emojis'] = save_emojis
        with open('guilds.json', 'w') as out_file:
            json.dump(data, out_file)
        print(message)
        await ctx.send(save_emojis)


def setup(bot):
    bot.add_cog(Config(bot))
