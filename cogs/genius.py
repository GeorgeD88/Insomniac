import discord
from discord.ext import commands
import lyricsgenius


bloodshotRed = 0xb10010
errorRed = 0xff0000
loadedGreen = 0x3cc80a
alertYellow = 0xffee00

gen = lyricsgenius.Genius("0WltQQ-KU7qytdv4y1RR-pvGqmiIZf9B7iMi8TFqZuanDc2qAH3byfOmoqOl-PhG")


class Genius(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command()
    async def lyrics(self, ctx, *args):

        """
        Searches genius for lyrics

        SONG NAME
        or
        SONG NAME by ARTIST
        """

        song = ''
        artist = ''

        if 'by' in args:
            by = args.index('by')
            for i in range(by):
                song += args[i].lower() + ' '
            for i in range(by + 1, len(args)):
                artist += args[i].lower() + ' '
        else:
            for word in args:
                song += word.lower() + ' '
            song = song[:-1]
            artist = artist[:-1]

        search = gen.search_song(title=song, artist=artist)
        lyr = search.lyrics
        if len(lyr) > 2000:
            lyr = lyr[:1997] + '...'
        await ctx.send(lyr)


def setup(bot):
    bot.add_cog(Genius(bot))
