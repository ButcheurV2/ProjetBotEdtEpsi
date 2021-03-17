import discord
from discord.ext import commands
from datetime import date
import datetime
from datetime import datetime
from selenium import webdriver
from time import sleep
import os

TOKEN = os.getenv('TOKEN')

print(TOKEN)

bot = commands.Bot(command_prefix='!')
today = date.today()

@bot.event
async def on_ready():
  print("Bot prêt !")
  activity = discord.Game(name="Utilise !aide")
  await bot.change_presence(status=discord.Status.dnd, activity=activity)


@bot.command()
async def aide(ctx):
  await ctx.send("Synthaxe de la commande : !edt prenom.nom" + "\n"
                 + "Pour voir l'edt pour une date précise, utilisez : !edt prenom.nom mois/jour/année" +
                 "\n" + "Exemple, !edt jean.valjean 25/04/2021 (25 avril 2021)")


@bot.command()
async def edt(ctx, msg=None, dateEdt=None):
    if msg is None:
        await ctx.send("Erreur synthaxe : essaye '!edt prenom.nom' ! ")
    if "." not in msg:
        await ctx.send("Login incorrect, exemple de login : jean.valjean")
    elif dateEdt is None:
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date={date}".format(
            date=today.strftime("%m/%d/%Y"))
        takeScreen(urlObtenu)
        await ctx.send(urlObtenu)
        await ctx.send(file=discord.File('test.png'))
    else:
        try:
            date_obj = datetime.strptime(dateEdt, '%d/%m/%Y').date()
            date_obj_fin = date_obj.strftime("%m/%d/%Y")
        except ValueError:
            await ctx.send("Erreur format de la date, essaye 10/05/2021 par exemple.")
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date=" + str(date_obj_fin)
        takeScreen(urlObtenu)
        await ctx.send(urlObtenu)
        await ctx.send(file=discord.File('test.png'))
def takeScreen(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options )
    driver.get(url)
    sleep(1)
    driver.get_screenshot_as_file("test.png")
    driver.quit()
    print("Fichier envoyé")
bot.run(TOKEN)

