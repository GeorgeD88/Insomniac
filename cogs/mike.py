import discord
from discord.ext import commands
from random_word import RandomWords
from time import sleep


random = RandomWords()


class Mike(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yall(self, ctx):
        await ctx.send('Y\'all really are some annoying motherfuckers :skull:')

    @commands.command()
    async def cg(self, ctx):
        adj = None
        found = False

        while not found:
            print('trying...')
            try:
                adjs = random.get_random_words(includePartOfSpeech='adjective', limit=60)
                for a in adjs:
                    if a.lower()[0] == 'c':
                        adj = a
                        found = True
            except Exception as e:
                print(e)
                print('GIVE HIM A SEC')
                sleep(5)
        print('found adjective')

        noun = None
        found = False

        while not found:
            print('trying...')
            try:
                nouns = random.get_random_words(includePartOfSpeech='noun', limit=60)
                for n in nouns:
                    if n.lower()[0] == 'g':
                        noun = n
                        found = True
            except Exception as e:
                print(e)
                print('GIVE HIM A SEC')
                sleep(5)
        print('found noun')

        await ctx.send(f'{adj} {noun}')

    @commands.command()
    async def masscg(self, ctx, extension: int = 3):
        adjs = random.get_random_words(includePartOfSpeech='adjective', limit=500)
        print('generated adjective list')
        nouns = random.get_random_words(includePartOfSpeech='noun', limit=500)
        print('generated noun list')

        if extension == 0:
            for i in range(extension):
                adjs.extend(random.get_random_words(includePartOfSpeech='adjective', limit=500))
                print('adjective list extension #' + str(i+1))
                adjs.extend(random.get_random_words(includePartOfSpeech='noun', limit=500))
                print('noun list extension #' + str(i+1))
                sleep(5)

        refined_a = []
        for a in adjs:
            if a.lower()[0] == 'c':
                refined_a.append(a)
        print('refined adjectives')
        print(len(refined_a))

        refined_n = []
        for n in nouns:
            if n.lower()[0] == 'g':
                refined_n.append(n)
        print('refined nouns')
        print(len(refined_n))

        top = len(refined_a) if len(refined_a) < len(refined_n) else len(refined_n)
        text = ''

        for i in range(top):
            text += f'{refined_a[i]} {refined_n[i]}\n'
        print('generated text')

        #with open('cg.txt', 'w+') as out_file:
        #    out_file.write(text)
        #print('exported to text file')

        #await ctx.send(file=discord.File('cg.txt'))
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Mike(bot))
