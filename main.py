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
import urllib.parse
from urllib.parse import urlparse
from datetime import timedelta
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
    else:
        try:
            date_obj = datetime.strptime(dateEdt, '%d/%m/%Y').date()
            date_obj_fin = date_obj.strftime("%m/%d/%Y")
        except ValueError:
            await ctx.send("Erreur format de la date, essaye 10/05/2021 par exemple.")
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date=" + str(date_obj_fin)
        takeScreen(urlObtenu)
        print(urlObtenu)
        await ctx.send(file=discord.File('test.png'))
@client.command()
async def teams(ctx, msg=None):
    if msg is None:
        await ctx.send("Erreur synthaxe : essaye '!teams prenom.nom' ! ")
    if "." not in msg:
        await ctx.send("Login incorrect, exemple de login : jean.valjean")
    else:
        urlObtenu = "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=" + msg + "&date={date}".format(
            date=today.strftime("%m/%d/%Y"))
        print(urlObtenu)
#        await ctx.send("Génération de ton URL Teams. . . . . . . .")
        lienTeams(urlObtenu)
        if lienConvoTeams==" ":
            await ctx.send("Aucun lien disponible actuellement")
        else:
            await ctx.send("Lien teams de ton cours actuel : " + lienConvoTeams)
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
    links = soup.findAll('a', href=True)
    tabLienFinal = []
    now = datetime.now()
    dateJ = now.strftime("%m/%d/%Y")
    dateJPlusUn = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y')
    lien = 0
    for link in links:
        lien += 1
        tabLien = link['href']
        params = urllib.parse.parse_qs(urllib.parse.urlparse(tabLien).query)
        if now.hour == 6 or now.hour == 8 and params['date'][-1] == dateJ:
            tabLienFinal.append(link['href'])
        elif now.hour == 11 or now.hour == 13 and params['date'][-1] == dateJPlusUn:
            tabLienFinal.append(link['href'])
    print(tabLienFinal[0])
    if tabLienFinal is not None:
        lienConvoTeams = tabLienFinal[0]
    else:
        lienConvoTeams = " "
#Tâche qui se lance toute les heures pour donner le lien teams du cours actuel
@tasks.loop(seconds=3600)
async def mytask(msg):
     now = datetime.now()
     print(now.hour)
     jour = now.strftime("%A")
     if jour == "Sunday" or jour == "Saturday":
         print("C'est le W-E")
     else:
         if now.hour == 6 or now.hour == 8 or now.hour == 11 or now.hour == 13:
             channel = client.get_channel(822221243276984371)
             lienTeams("https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel="+msg+"&date={date}".format(date=today.strftime("%m/%d/%Y")))
             await channel.send("Lien de la conv Teams actuel : " + lienConvoTeams)
         else:
             print("Yo")
client.run(TOKEN)

