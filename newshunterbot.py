import urllib2
import re
from tabulate import tabulate
from bs4 import BeautifulSoup
import time
import telepot


ktopics=[['News'],['Business'],['Entertainment'],['Sport'],['Sci-Tech']]
topics=['News','Business','Entertainment','Sport','Sci-Tech']
ksubtopics=[[['News'], ['National'], ['International'], ['Andhra Pradesh'], ['Karnataka'], ['Kerala'], ['Tamil Nadu'], ['Telangana'], ['Other states'], ['Delhi']], [['Business'], ['Agri-Business'], ['Economy'], ['Industry'], ['Markets']], [['Entertainment'], ['Art'], ['Cinema'], ['Dance'], ['History & Culture'], ['Music'], ['Theatre']], [['Sport'], ['Cricket'], ['Football'], ['Hockey'], ['Tennis'], ['Races'], ['Other Sports']], [['Sci-Tech'], ['Environment'], ['Health'], ['Science'], ['Technology'], ['Gadgets'], ['Internet']]]
subtopics=[['News', 'National', 'International', 'Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana', 'Other states', 'Delhi'], ['Business', 'Agri-Business', 'Economy', 'Industry', 'Markets'], ['Entertainment', 'Art', 'Cinema', 'Dance', 'History & Culture', 'Music', 'Theatre'], ['Sport', 'Cricket', 'Football', 'Hockey', 'Tennis', 'Races', 'Other Sports'], ['Sci-Tech', 'Environment', 'Health', 'Science', 'Technology', 'Gadgets', 'Internet']]
mylinks=[['http://www.thehindu.com/news/', 'http://www.thehindu.com/news/national/', 'http://www.thehindu.com/news/international/', 'http://www.thehindu.com/news/national/andhra-pradesh/', 'http://www.thehindu.com/news/national/karnataka/', 'http://www.thehindu.com/news/national/kerala/', 'http://www.thehindu.com/news/national/tamil-nadu/', 'http://www.thehindu.com/news/national/telangana/', 'http://www.thehindu.com/news/national/other-states/', 'http://www.thehindu.com/news/cities/Delhi/'],[ 'http://www.thehindu.com/business/', 'http://www.thehindu.com/business/agri-business/', 'http://www.thehindu.com/business/Economy/', 'http://www.thehindu.com/business/Industry/', 'http://www.thehindu.com/business/markets/'],[ 'http://www.thehindu.com/entertainment/', 'http://www.thehindu.com/entertainment/entertainment-art/', 'http://www.thehindu.com/entertainment/entertainment-cinema/', 'http://www.thehindu.com/entertainment/entertainment-dance/', 'http://www.thehindu.com/entertainment/entertainment-history/', 'http://www.thehindu.com/entertainment/entertainment-music/', 'http://www.thehindu.com/entertainment/entertainment-theatre/'],[ 'http://www.thehindu.com/sport/', 'http://www.thehindu.com/sport/cricket/', 'http://www.thehindu.com/sport/football/', 'http://www.thehindu.com/sport/hockey/', 'http://www.thehindu.com/sport/tennis/', 'http://www.thehindu.com/sport/races/', 'http://www.thehindu.com/sport/other-sports/'],[ 'http://www.thehindu.com/sci-tech/', 'http://www.thehindu.com/sci-tech/energy-and-environment/', 'http://www.thehindu.com/sci-tech/health/', 'http://www.thehindu.com/sci-tech/science/', 'http://www.thehindu.com/sci-tech/technology/', 'http://www.thehindu.com/sci-tech/technology/gadgets/', 'http://www.thehindu.com/sci-tech/technology/internet/']]

stage=0
intopic=0
insubtopic=0

def shownews(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    links=[]

    if(url.find('http://www.thehindu.com/entertainment/') != -1):
     url2='http://www.thehindu.com/entertainment/'
    else:
     url2=url   
    for x in soup.findAll('div'):
      try:
        for y in x.findAll('h1'):
           if( y.a['href'] not in links and y.a['href'].find(url2) !=-1):
            links.append(y.a['href'])  
        for y in x.findAll('h2'): 
           if( y.a['href'] not in links and y.a['href'].find(url2) !=-1):
            links.append(y.a['href'])  
        for y in x.findAll('h3'):
           if( y.a['href'] not in links and y.a['href'].find(url2) !=-1):
            links.append(y.a['href'])
      except Exception:
        continue
    print len(links)
    return links


   
def handle(msg):
    global stage
    global intopic
    global insubtopic
    
    chat_id = msg['chat']['id']
    command = msg['text']
    username = msg['from']['first_name']
    print "Got command:"+command

    if command == '/start':
      bot.sendMessage(chat_id, 'Hi, '+username+'. Type /topics to get the news topics.')       
    elif command == '/topics':
      stage=1  
      mainkeyboard = {'keyboard': ktopics}
      bot.sendMessage(chat_id, 'Choose a topic:', reply_markup=mainkeyboard)
    elif command[0] != '/' and stage==1:
      stage=2
      intopic=topics.index(command)
      subkeyboard = {'keyboard': ksubtopics[intopic]}
      bot.sendMessage(chat_id, 'Choose a subtopic:', reply_markup=subkeyboard)
    elif command[0] != '/' and stage == 2:
      insubtopic=subtopics[intopic].index(command)
      links=shownews(mylinks[intopic][insubtopic])
      if(len(links) == 0):
        bot.sendMessage(chat_id,'Sorry,no latest news to show in this category :(')
        return
      count=0
      for x in links:
         try: 
          bot.sendMessage(chat_id,'[Click to read full story]('+x+')',parse_mode='Markdown')
          count+=1
          if(count == 7):
              break
         except Exception:
          continue   
      

if __name__ == "__main__":
    bot = telepot.Bot('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print 'I am listening ...'
    bot.setWebhook()
    bot.message_loop(handle)
    while 1:
      time.sleep(10)
      

