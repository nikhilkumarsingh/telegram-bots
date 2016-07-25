from datetime import datetime
import telepot
import time
import requests
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

key="AIzaSyApuFoKxVMRQ2einlsA0rkx2S4WJjJIh34"  

def getLatLng(address):
  geo_s ='https://maps.googleapis.com/maps/api/geocode/json'
  param = {'address': address, 'key': key}
  response = requests.get(geo_s, params=param)
  json_dict = response.json()
  lat = json_dict['results'][0]['geometry']['location']['lat'] 
  lng = json_dict['results'][0]['geometry']['location']['lng']
  properAddr=json_dict['results'][0]['formatted_address']
  print properAddr
  return lat,lng,properAddr

def NearbySearch(lat,lng,keyword,radius=500):
  url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
  url+="location=%f,%f&" % (lat,lng)
  url+="radius=%i&" % radius
  url+="type=%s&" % keyword
  url+="key=%s" % key
  response=requests.get(url)
  json_dict=response.json()
  res=json_dict['results']
  info_pack=[]
  
  for x in res:
    info=[]
    info.append(x['name']+' '+x['vicinity'])
    if(x.has_key('rating')):
      info.append(x['rating'])
    else:
      info.append('N/A')
    info.append(x['geometry']['location']['lat'])
    info.append(x['geometry']['location']['lng'])
    info_pack.append(info)  
  return info_pack  
  
def getStaticMap(lat,lng,zoom=15,maptype='roadmap'): 
  url="http://maps.google.com/maps/api/staticmap?"
  center=str(lat)+","+str(lng)
  url += "center=%s&" % center
  url += "zoom=%i&" % zoom       #range 0 to 22
  url += "maptype=%s&" % maptype
  url += "scale=1&"
  url += "size=320x320&"
  url += "format=jpg&"
  url += "sensor=false&" 
  url+="markers=size:mid|color:red|label:C|%s,%s|&" %(lat,lng)
  r=requests.get(url)
  chunk_size=1000
  fd=open('mymap.jpg', 'wb') 
  for chunk in r.iter_content(chunk_size):
    fd.write(chunk)
  fd.close()

def getPhoto(photoreference,maxwidth=800):
  url="https://maps.googleapis.com/maps/api/place/photo?"
  url+="maxwidth=%i&" % maxwidth
  url+="photoreference=%s&" % photoreference
  url+="key=%s" % key
  r=requests.get(url)
  chunk_size=1000
  fd=open('myimage.jpg', 'wb') 
  for chunk in r.iter_content(chunk_size):
    fd.write(chunk)
  fd.close()

  
stage=0
location=''
maptype=''
mapsize=0
def handle(msg):
    global stage
    global location
    global maptype
    chat_id = msg['chat']['id']
    try:
      command = msg['text']
      print 'Got command: %s' % command
    except Exception:
      lat,lng=msg['location']['latitude'],msg['location']['longitude']
      getStaticMap(lat,lng,20,"roadmap")
      return
      
    if command == '/locate':
       markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Share my location with bot.', request_location=True)]])
       bot.sendMessage(chat_id,reply_markup=markup)
    elif command == '/getmap':
       stage=1
       bot.sendMessage(chat_id, 'Enter location:')
    elif stage == 1:
       stage=2
       location=command
       mainkeyboard = {'keyboard': [['roadmap'],['satellite'],['terrain'],['hybrid']]}
       bot.sendMessage(chat_id, 'Choose a view:', reply_markup=mainkeyboard)
    elif stage == 2:
       stage=3
       maptype=command
       mainkeyboard = {'keyboard': [['5'],['10'],['15'],['20']]}
       bot.sendMessage(chat_id, 'Choose map size:', reply_markup=mainkeyboard)   
    elif stage == 3:
       bot.sendChatAction(chat_id, 'upload_photo')
       mapsize=int(command)
       lat,lng,properAddr=getLatLng(location)
       getStaticMap(lat,lng,mapsize,maptype)
       f=open('mymap.jpg','rb')
       bot.sendPhoto(chat_id,f,caption=properAddr)
       f.close()

       
print "I am Listening...."
bot = telepot.Bot('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
bot.message_loop(handle)
while 1:
 time.sleep(10)


'''
maptype='satellite'
Location=raw_input()
lat,lng=getLatLng(Location)
getStaticMap(lat,lng,10,maptype)

maptype:roadmap,hybrid,terrain,satellite
'''



'''
accounting
airport
amusement_park
aquarium
art_gallery
atm
bakery
bank
bar
beauty_salon
bicycle_store
book_store
bus_station
    cafe
    campground
    car_dealer
    car_rental
    car_repair
    car_wash
    casino
    cemetery
    church
    city_hall
    clothing_store
    convenience_store
    courthouse
    dentist
    department_store
    doctor
    electrician
    electronics_store
    embassy
    establishment (deprecated)
    finance (deprecated)
    fire_station
    florist
    food (deprecated)
    funeral_home
    furniture_store
    gas_station
    general_contractor (deprecated)
    grocery_or_supermarket
    gym
    hair_care
    hardware_store
    health (deprecated)
    hindu_temple
    home_goods_store

    hospital
    insurance_agency
    jewelry_store
    laundry
    lawyer
    library
    liquor_store
    local_government_office
    locksmith
    lodging
    meal_delivery
    meal_takeaway
    mosque
    movie_rental
    movie_theater
    moving_company
    museum
    night_club
    painter
    park
    parking
    pet_store
    pharmacy
    physiotherapist
    place_of_worship (deprecated)
    plumber
    police
    post_office
    real_estate_agency
    restaurant
    roofing_contractor
    rv_park
    school
    shoe_store
    shopping_mall
    spa
    stadium
    storage
    store
    subway_station
    synagogue
    taxi_stand
    train_station
    transit_station
    travel_agency
    university
    veterinary_care
    zoo
'''
