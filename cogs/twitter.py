import discord
from discord.ext import commands
import configuration
import requests
import tweepy
import json


bloodshotRed = 0xb10010
errorRed = 0xff0000
loadedGreen = 0x3cc80a
alertYellow = 0xffee00

auth = tweepy.OAuthHandler(configuration.api_key, configuration.api_secret_key)  # authentication of consumer key and secret
auth.set_access_token(configuration.access_token, configuration.access_token_secret)  # authentication of access token and secret
api = tweepy.API(auth)


class Twitter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command()
    async def tweet(self, ctx, *args):
        if ctx.message.author.id != configuration.owner_id:
            embed = discord.Embed(title=':stop_sign: **Access Restricted:** Only G-Unit himself can use this command', color=errorRed)
            await ctx.send(embed=embed)
            print(f'Access was restricted from {ctx.message.author}')
            return

        post = ''
        for w in args:
            post += w + ' '
        post = post[:-1]

        api.update_status(status=post)
        await ctx.send('Tweeted: ' + post)
        print('Tweeted: ' + post)

    @commands.command()
    async def last(self, ctx, user):
        api_user = api.get_user(user)
        user_json = api_user._json
        last_tweet = api.user_timeline(screen_name=user)

        #with open('output.json', 'w+') as out_file:
        #    json.dump(last_tweet[0]._json, out_file, indent=2)

        url = user_json['status']['entities']['urls'][0]['expanded_url']
        await ctx.send(f"@{user}'s last tweet: {url}")


def setup(bot):
    bot.add_cog(Twitter(bot))
