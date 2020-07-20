import discord
from discord.ext import commands
from PIL import Image
import os
import pyautogui as gui
from time import sleep
import datetime
import win32com.client


online = False


class Simp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def simp(self, ctx, fname: str, lname: str, bmonth: str, bday: str, byear: str, feet: int, inches: int, gender: str, country: str, job: str):

        """First Name, Last Name, Birthmonth (in numbers), Birthday, Birthyear, height (feet), height (inches), gender (letter), nationality, job"""

        if not online:
            await ctx.send('Command currently offline')
            return
        # Restricts to only server Sigma Apple Pie
        #if ctx.guild.id != 717971011609296927:
        #    await ctx.send('Command removed')
        #    return

        # Date stuff
        today = datetime.date.today()
        date = f'{str(today.month).zfill(2)}/{str(today.day).zfill(2)}/{today.year}'

        # Avatar stuff
        gif = ctx.message.author.is_avatar_animated()
        extension = 'gif' if gif else 'png'
        with open('avatar.' + extension, 'wb') as out_file:
            await ctx.message.author.avatar_url.save(out_file)
        if gif:
            img = Image.open('avatar.gif')
        else:
            img = Image.open('avatar.png')
        img.save('avatar.png', 'png', optimize=True, quality=70)
        # os.remove('avatar.gif')

        # Photoshop
        PS = win32com.client.Dispatch("Photoshop.Application")
        PS.Open(r"C:\Users\Georg\Documents\simp_test.psd")

        layers = PS.Application.ActiveDocument

        gui.click(1005, 935)  # Focus file
        gui.doubleClick(820, 555)  # Double click frame
        sleep(0.1)
        gui.click(45, 10)  # File
        gui.click(140, 405)  # Place embedded
        sleep(0.3)
        gui.typewrite('avatar.png')  # Open file
        gui.press('Enter')

        dob = layers.ArtLayers['DOB']
        dobText = dob.TextItem
        dobText.contents = f'{bmonth.zfill(2)}/{bday.zfill(2)}/{byear}'

        issue = layers.ArtLayers['Issue Date']
        issueText = issue.TextItem
        issueText.contents = date

        height = layers.ArtLayers['Height']
        heightText = height.TextItem
        heightText.contents = f'{feet}\'{inches}"'

        sex = layers.ArtLayers['Sex']
        sexText = sex.TextItem
        sexText.contents = gender.upper()

        firstName = layers.ArtLayers['Name']
        firstNameText = firstName.TextItem
        firstNameText.contents = f'{fname} {lname}'

        nationality = layers.ArtLayers['Nationality']
        nationalityText = nationality.TextItem
        nationalityText.contents = country

        occupation = layers.ArtLayers['Occupation']
        occupationText = occupation.TextItem
        occupationText.contents = job

        options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        options.Format = 6  # JPEG
        options.Quality = 100  # Value from 0-100

        path = r"C:\Users\Georg\Pictures"
        img_name = f'{fname}_{lname[0]}_Simp_ID.jpg'

        layers.Export(ExportIn=path + img_name, ExportAs=2, Options=options)

        file = discord.File(fp=path + img_name)
        await ctx.send(file=file)

        print(f'{fname}_{lname[0]}_Simp_ID Generated')


def setup(bot):
    bot.add_cog(Simp(bot))
