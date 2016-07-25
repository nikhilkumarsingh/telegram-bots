import telepot
import urllib2
import time
import re
import os
import codecs
from bs4 import BeautifulSoup
from tabulate import tabulate


allcontests=[]
digits=['0','1','2','3','4','5','6','7','8','9']


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    username = msg['from']['first_name']

    print 'Got command: %s from %s' % (command,username)

    if command == '/start':
           bot.sendMessage(chat_id,"Hi,"+username+" !\nType /present,/past or /future to see contests.\nType /rank <username> to check your rank.\nType /contest <contest-code> to see contest problems.\nType /problem <contest-name> <problem-code> to download a contest-problem in a text file.")
           return
    if command == '/present':
        if(allcontests[0] == None):
           bot.sendMessage(chat_id,"No contests to show.")
        else:   
           bot.sendMessage(chat_id,create_table(allcontests[0],"Present Contests"))
    elif command == '/future':
        if(allcontests[1] == None):
           bot.sendMessage(chat_id,"No contests to show.")
        else: 
           bot.sendMessage(chat_id,create_table(allcontests[1],"Future Contests"))
    elif command == '/past':
        if(len(allcontests[2]) == None):
           bot.sendMessage(chat_id,"No contests to show.")
        else: 
           bot.sendMessage(chat_id,create_table(allcontests[2],"Past Contests"))
    elif command[:5] == '/rank':
           try:
             user=command.split(' ')[1]
           except Exception:
             bot.sendMessage(chat_id,"Please enter the query in this format:\n/rank <username>")
           bot.sendMessage(chat_id,"Fetching rank of "+user+" ....")
           bot.sendMessage(chat_id,show_rank(user))
    elif command[:8] == '/contest':
           cname=command.split(' ')[1]
           bot.sendMessage(chat_id,show_problems(cname))
    elif command[:8] == '/problem':
         try:
           concode,pcode=command.split(' ')[1],command.split(' ')[2]
         except Exception:
            bot.sendMessage(chat_id,"Please enter the query in this format:\n/problem <contest-code> <problem-code>")
            return
         f=open(pcode+'.txt','w')
         ptext=get_problem_text(concode,pcode)
         if(ptext == '0'):
            print "Sorry, no such problem exists!"
            return
         f.write(ptext)
         f.close()
         res=bot.sendDocument(chat_id,open(pcode+'.txt','rb'))
         os.remove(pcode+'.txt')
    bot.sendMessage(chat_id,"Anything else, "+username+"?")


def create_table(contests,ctype):
    return "\n-------------------------\n".join(x for x in contests)
    

def find_contests():
   url ="http://www.codechef.com/contests"
   response = urllib2.urlopen(url)
   html = response.read()
   soup = BeautifulSoup(html,'lxml')
   print "parsed"
   count=0
   for x in soup.findAll('tbody'):
       contests=[]
       k=0
       for row in x.findAll('tr'):
          comp=''
          for info in row.findAll('td'):
              if(len(info.get_text())>0):
                 comp+=(info.get_text().encode("utf-8"))+"\n"
          if(len(comp)>0):      
            contests.append(comp)
          k+=1    
          if(k>5):
            break
       allcontests.append(contests)    
       count+=1
       if(count == 3):
          break
   if(len(allcontests) == 2):
     allcontests.append([])
     allcontests[2]=allcontests[1]
     allcontests[1]=None
     

def show_problems(concode):
   url ="http://www.codechef.com/"+concode
   response = urllib2.urlopen(url)
   html = response.read()
   soup = BeautifulSoup(html,'lxml')
   print "parsed"
   problems=[]
   for x in soup.findAll('tbody'):
       for y in x.findAll('tr'):
           ques=[]
           for p in y.findAll('td'):
               ques.append(p.get_text().encode("utf-8").replace("\n",""))    
           problems.append(ques)
   p=[]
   for x in problems:
      p.append(x[1]+"("+x[2]+")")        
   return "Problem-Code(Successful Submissions)\n------------------------------------------------------------\n"+"\n".join(x for x in p)


def get_problem_text(concode,pcode):
   try:
     url ="http://www.codechef.com/"+concode+"/problems/"+pcode
     response = urllib2.urlopen(url)
     html = response.read()
     soup = BeautifulSoup(html,'lxml')
   except Exception:
     return '0'
   
   flag=0
   mytext=''
   for x in soup.findAll('div',attrs={'class':'content'}):
     if(x.get_text().find('Read problems statements in Mandarin Chinese, Russian and Vietnamese as well.') != -1):
      mytext = x.get_text()
   mytext.replace('\u2264','<=')
   return mytext.encode('utf-8')

def show_rank(username):
     allranks=[]
     url ="https://www.codechef.com/users/"+username
     response = urllib2.urlopen(url)
     html = response.read()
     soup = BeautifulSoup(html)  
     contype=["Long","Short","LTime"]
     for rtype in soup.findAll(attrs={'id':'hp-sidebar-blurbRating'}):
        for rows in rtype.findAll('tr'):
           ranks=[]
           ranks.append('')
           for col in rows.findAll('td'):
              rank=col.get_text().encode("utf-8")
              if(rank[0] in digits):
                rank=re.sub('[^0-9./]','',rank) 
                ranks.append(rank)     
           if(len(ranks)>1):
              allranks.append(ranks)

     for x in range(3):
        allranks[x][0]=contype[x]      
       
     return tabulate(allranks,headers=["Type","Rank","Rating"],tablefmt="plain")          




if __name__ == "__main__":
    find_contests()
    bot = telepot.Bot('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    bot.message_loop(handle)
    print 'I am listening ...'

    while 1:
      time.sleep(10)
    raw_input()







