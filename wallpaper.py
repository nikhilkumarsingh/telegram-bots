import urllib2
import random
import re
from tabulate import tabulate
from bs4 import BeautifulSoup
import time
import telepot
import os

cat=[u'abstract', u'animals', u'anime', u'architecture', u'auto', u'background', u'brands', u'cartoon', u'cinema', u'fantasy', u'food', u'funny', u'games', u'holidays', u'insects', u'landscape', u'objects', u'people', u'pictures', u'plants',  u'sports', u'transport']
subcat=[[u'background\nart\npatterns\nwater\npictures\npeople\ngirls\nplanets\nart\nphoto'], [u'cats\ndogs\nbirds\npictures\nhorses\ntigers\nwolfs\nleopards\nsea\n\n\n'], [u'\n\ngirls\nsexy\nmen\nvocaloids\nmiku\nhatsune\nmusic\nangels\ncartoon\nweapon\n\n\n'], [u'\n\nlandscape\ncities\nhouses\ncastles\nnight\nbridges\nrivers\neiffel\ntower\nsky\n\n\n'], [u'\n\ntransport\nbmw\nmersedes\nroads\naudi\ngirls\npeople\ntuning\nporsche\n\n\n'], [u'\n\nplants\nlogos\nflowers\nholidays\npatterns\ndrops\nabstract\nbrands\nnew\nyear\n\n\n'], [u'\n\nlogos\nbackground\napple\nwindows\ndrinks\nandroid\nauto\nfunny\nfood\n\n\n'], [u'\n\nanime\ngirls\nbackground\npictures\nfunny\nice\nage\nmasha\nand\nthe\nbear\nmen\nanimals\n\n\n'], [u'\n\npeople\nactors\nmen\ngirls\nbatman\nhouse\nm.d.\niron\nman\nstar\nwars\njoker\n\n\n'], [u'\n\ngirls\npeople\nsexy\nlandscape\nart\ndragons\npictures\nplanets\nuniverse\n\n\n'], [u'\n\nfruits\ndrinks\ndessert\nberries\nstrawberry\nbackground\ncoffee\napples\nholidays\n\n\n'], [u'\n\nanimals\npictures\nbackground\npeople\ncats\ncartoon\nmen\nart\ngirls\n\n\n'], [u"\n\ngirls\nmen\npeople\nassassin's\ncreed\npictures\nmortal\nkombat\nbackground\nlara\ncroft:\ntomb\nraider\nfantasy\n\n\n"], [u"\n\nnew\nyear\nchristmas,\nxmas\nbackground\nvalentine's\nday\nhearts\nlove\nfir-trees\ntoys\npictures\n\n\n"], [u'\n\nbutterflies\nladybugs\nflowers\nplants\nbees\npictures\nspiders\nart\ngrass\n\n\n'], [u'\n\ntrees\nsea\nsky\nrivers\nmountains\nsunset\ncities\nclouds\nwater\n\n\n'], [u'\n\njewelry\nmusic\nweapon\nclock\nbackground\nchess\ntoys\nstill\nlife\ntools\n\n\n'], [u'\n\ngirls\nsexy\nactors\nmen\nmusic\nartists\ncinema\ntits\npictures\n\n\n'], [u'\n\ngirls\npeople\nlandscape\nanimals\nsexy\nart\nbackground\nmen\nfunny\n\n\n'], [u'\n\nflowers\nroses\nbackground\nleaves\ntrees\nlandscape\ntulips\ndrops\nbouquets\n\n\n'], [u'\n\npeople\nfootball\nmen\ntransport\nauto\nlogos\nraces\ngirls\nbasketball\n\n\n'], [u'\n\nauto\nairplanes\nbmw\nweapon\nmersedes\nsea\nships\nroads\naudi\n\n\n']]

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    username = msg['from']['first_name']
    print 'Got command: %s' % command

    if command == '/start':
           bot.sendMessage(chat_id,"Hi,"+username+" !\n Type /cat to see available categories.\n Type /subcat <category> to see subcategories.\n Type /search <category> <subcategory> to search for images.")
           return
    elif command == '/cat':   
           bot.sendMessage(chat_id,"\n".join(x for x in cat))
           bot.sendMessage(chat_id,"Type /subcat <category> to see subcategories.")
    elif command[:7] == '/subcat':
           category=command.split(' ')[1]
           try: 
             ind=cat.index(category)
             bot.sendMessage(chat_id,"\n".join(x for x in subcat[ind]))
             bot.sendMessage(chat_id,"Type /search <category> <subcategory> to search for images.")
           except Exception:
             bot.sendMessage(chat_id,"Sorry no such category found!") 
    elif command[:7] == '/search':
           query=command.split(' ',1)[1]
           query=query.replace(" ","+")
           result=find_links(query)
           index=random.randrange(0,len(result),2)
           result[index]=result[index].replace("111x185","preview")
           filename=str(len(os.listdir(os.getcwd())))+".jpg"
           f = open(filename,'wb')
           f.write(urllib2.urlopen(result[index]).read())
           f.close()
           f = open(filename,'rb')
           response = bot.sendPhoto(chat_id,f)
           f.close()
           
           

def find_links(tags):
   url ="http://wallpaper.mob.org/gallery/tag="+tags
   response = urllib2.urlopen(url)
   html = response.read()
   soup = BeautifulSoup(html)
   links=[]
   for x in soup.findAll('li',attrs={'class':'item'}):
      links.append(x.img['src'])
   return links

if __name__ == "__main__":
    os.getenv('PORT', '8080')
    os.getenv('IP', '0.0.0.0')
    bot = telepot.Bot('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    bot.message_loop(handle)
    print 'I am listening ...'
    while 1:
      time.sleep(10)
    raw_input()


