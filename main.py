import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date
import datetime
from datetime import datetime
from selenium import webdriver
from time import sleep
import os
import requests
from bs4 import BeautifulSoup

#Obtention du token discord que l'on a set dans notre environement
TOKEN = os.getenv('TOKEN')
#Variable global du lien Teams
global lienConvoTeams
#On récupère la date
today = date.today()
#On initialise le préfixe de commande du bot
client = commands.Bot(command_prefix = '!')
#Fonction quand le bot se lance
@client.event
async def on_ready():
  print("Bot prêt !")
  activity = discord.Game(name="Utilise !aide")
  await client.change_presence(status=discord.Status.dnd, activity=activity)
  channel = client.get_channel(822221243276984371) #On connecte le bot grâce à l'id du channel
#Commande aide
@client.command()
async def aide(ctx):
  await ctx.send("Synthaxe de la commande : !edt prenom.nom" + "\n"
                 + "Pour voir l'edt pour une date précise, utilisez : !edt prenom.nom jour/mois/année" +
                 "\n" + "Exemple, !edt jean.valjean 25/04/2021 (25 avril 2021)")
#Commande lien
@client.command()
async def lien(ctx, msg=None):
    if msg is None:
        await ctx.send("Erreur synthaxe : essaye '!lien prenom.nom' ! ")
    if "." not in msg:
        await ctx.send("Login incorrect, exemple de login : jean.valjean")
    else:
        mytask.start(msg) #On lance la tâche automatisée

#Commande edt
@client.command()
async def edt(ctx, msg=None, dateEdt=None):
    global lienConvoTeams
    if msg is None:
        await ctx.send("Erreur synthaxe : essaye '!edt prenom.nom' ! ")
    if "." not in msg:
        await ctx.send("Login incorrect, exemple de login : jean.valjean")
    elif dateEdt is None:
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date={date}".format(
            date=today.strftime("%m/%d/%Y"))
        takeScreen(urlObtenu)
        await ctx.send(file=discord.File('test.png'))
        await ctx.send("Génération de ton URL Teams. . . . . Veuillez patienter 45 secondes . . . .")
        sleep(45)
        lienTeams("https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date={date}".format(
            date=today.strftime("%m/%d/%Y")))
        await ctx.send("Lien Teams de ton cours actuel : " + lienConvoTeams)
    else:
        try:
            date_obj = datetime.strptime(dateEdt, '%d/%m/%Y').date()
            date_obj_fin = date_obj.strftime("%m/%d/%Y")
        except ValueError:
            await ctx.send("Erreur format de la date, essaye 10/05/2021 par exemple.")
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date=" + str(date_obj_fin)
        takeScreen(urlObtenu)
        await ctx.send(file=discord.File('test.png'))
#Fonction qui permet de prendre un screen de la page de l'edt
def takeScreen(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options )
    driver.get(url)
    sleep(3)
    driver.get_screenshot_as_file("test.png")
    driver.quit()
    print("Fichier envoyé")
#Fonction qui renvoie le lien teams du cours actuel
def lienTeams(url):
    global lienConvoTeams
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    lien = 0
    tabLien = []
    for sexe in soup.find_all('a', {'href': True}):
        if (lien == 0 or lien % 4 == 0):
            tabLien.clear()
            tabLien.append(sexe['href'])
        lien += 1
    print(tabLien)
    lienConvoTeams = tabLien[0]
#Tâche qui se lance toute les heures pour donner le lien teams du cours actuel
@tasks.loop(seconds=3600)
async def mytask(msg):
     now = datetime.now()
     print(now.hour)
     if(now.hour == 7 or now.hour == 9 or now.hour == 12 or now.hour == 14):
         channel = client.get_channel(822221243276984371)
         lienTeams("https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel="+msg+"&date={date}".format(date=today.strftime("%m/%d/%Y")))
         await channel.send("Lien de la conv Teams actuel : " + lienConvoTeams)
     else:
        print("yo?")
client.run(TOKEN)

