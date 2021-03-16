import discord
from discord.ext import commands
from datetime import date
from selenium import webdriver
from time import sleep


TOKEN = 'TOKEN DU BOT DISCORD'

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
                 "\n" + "Exemple, !edt jean.valjean 04/25/2021 (25 avril 2021)")


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
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date=" + dateEdt
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
    print("end...")
bot.run(TOKEN)

