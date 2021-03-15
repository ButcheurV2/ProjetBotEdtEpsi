import discord
from discord.ext import commands
from datetime import date
from selenium import webdriver
from time import sleep


TOKEN = 'TOKEN DISCORD'

bot = commands.Bot(command_prefix='!')
today = date.today()

@bot.event
async def on_ready():
  print("Bot is ready")

@bot.command()
async def aide(ctx):
  await ctx.send("Synthaxe de la commande : $edt prenom.nom")

@bot.command()
async def edt(ctx, *msg):
    if len(msg) == 0:
      await ctx.send("Erreur synthaxe : essaye '$edt prenom.nom' ! ")
    msg = ctx.message.content.split(" ", 1)
    if "." not in msg[1]:
       await ctx.send("Login incorrect, exemple de login : jean.valjean")
    else:
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel="+msg[1]+"&date={date}".format(date=today.strftime("%m/%d/%Y"))
        takeScreen(urlObtenu)
        await ctx.send(urlObtenu)
        await ctx.send(file=discord.File('test.png'))

def takeScreen(url):
    driver = webdriver.Chrome("chemin chromedriver")
    driver.get(url)
    sleep(1)
    driver.get_screenshot_as_file("test.png")
    driver.quit()
    print("end...")
bot.run(TOKEN)

