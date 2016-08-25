import requests
import datetime
from datetime import timedelta
import sys
import time
import smtplib
import accountData
from email.MIMEText import MIMEText

maxLat = 22.78
minLat = 22.47
emailMaxLat = 22.695
emailMinLat = 22.66

deltaLat = 0.03

maxLong = 120.44
minLong = 120.245
emailMaxLong = 120.327
emailMinLong = 120.281

systemDetectIdentifier = "(Poke Radar Prediction)"
pokemonNewlyFoundIdentifier = "Success"

def getRequest(minLatitude, maxLatitude, minLongitude, maxLongitude):
    url = "https://www.pokeradar.io/api/v1/submissions?deviceId=e75a51005d0e11e6a5118f01dbbb3e30&minLatitude=%s&maxLatitude=%s&minLongitude=%s&maxLongitude=%s&pokemonId=0" % (
        minLatitude, maxLatitude, minLongitude, maxLongitude)
    return url

def sendEmail(sender, password,receiver, subject, content):
    msg = MIMEText(content)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(sender, password)
    mailServer.sendmail(sender, [receiver], msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

def pokemonDataToString(dict):
    s = "Pokemon No." + str(dict['pokemonId']) + " appear!\n"
    s += "Spawn Time: " + str(dict['created']) + ".\n"
    s += "Latitude: " + str(dict['latitude']) + "\n"
    s += "Longitude: " + str(dict['longitude']) + "\n"
    s += "On Google Map: https://www.google.com.tw/maps?q=%s,%s" % (dict['latitude'],dict['longitude'])

    return s

def withinEmailZone(pokemon):
    withinLat = (pokemon['latitude'] < emailMaxLat) and (emailMinLat < pokemon['latitude'])
    withinLong = (pokemon['longitude'] < emailMaxLong) and (emailMinLong < pokemon['longitude'])
    return withinLong and withinLat

table = [True ,True, True, True, True, True,
         True, True, True, True, False,
         False, True, False, False, True,
         False, False, True, False, True,
         #20
         False, True, False, True, True,
         True, True, True, False, False,
         True, False, False, True, True,
         True, True, True, True, True,
         #40
         True, True, False, True, True,
         False, True, False, True, True,
         True, True, True, False, True,
         True, True, True, True, False,
         #60
         True, True, True, True, True,
         True, True, True, False, True,
         True, False, True, True, True,
         True, True, True, False, True,
         #80
         True, True, True, True, True,
         True, True, True, True, True,
         True, True, True, True, True,
         True, True, False, True, True,
         #100
         True, False, True, True, True,
         True, True, True, True, True,
         True, True, True, True, True,
         False, True, False, True, False,
         #120
         True, True, True, True, True,
         True, False, True, False, True,
         True, True, True, True, True,
         True, True, True, True, True,
         #140
         True, True, True, True, True,
         True, True, True, True, True,
         True]

rareTable = [False ,False, False, True, False, False,
         True, False, False, True, False,
         False, False, False, False, False,
         False, False, False, False, False,
         #20
         False, False, False, False, False,
         True, False, False, False, False,
         False, False, False, False, False,
         False, False, True, False, False,
         #40
         False, False, False, False, False,
         False, False, False, False, False,
         False, False, False, False, False,
         False, False, False, False, False,
         #60
         False, False, False, False, True,
         False, False, False, False, False,
         False, False, False, False, False,
         False, False, False, False, False,
         #80
         False, False, False, False, False,
         False, False, False, False, False,
         False, False, False, True, False,
         False, False, False, False, False,
         #100
         False, False, False, False, False,
         True, True, True, False, False,
         False, False, True, False, False,
         False, False, False, False, False,
         #120
         False, False, False, False, False,
         False, False, False, False, True,
         True, True, False, True, True,
         True, True, False, False, False,
         #140
         True, True, True, True, True,
         True, False, False, True, True,
         True]

# mode 0, normal
# mode 1, hunting mode, only rare pokemon will be recorded
mode = 0

if __name__ == "__main__":
    mode = int(raw_input("Enter Mode: (0 for normal, 1 for hunting mode)"))

    nowMinLat = minLat

    while True:
        try:
            res = getRequest(nowMinLat, min(maxLat, nowMinLat+deltaLat), minLong, maxLong)
            response = requests.get(res)
            pokemons = response.json()
            #for all pokemons
            for pokemon in pokemons['data']:
                # if pokemon is system detected
                if pokemon['trainerName'] == systemDetectIdentifier:
                    # if the pokemon is the one we want to record
                    if ((mode==0 and table[pokemon['pokemonId']]) or (mode==1 and rareTable[pokemon['pokemonId']])):
                        spawnTime = datetime.datetime.fromtimestamp(int(pokemon['created']))
                        now = datetime.datetime.now()
                        notTooOutDated = (now - timedelta(minutes = 30) < spawnTime)
                        notInTheFuture = (spawnTime - timedelta(minutes = 30) < now)
                        withinLat = (pokemon['latitude'] < maxLat) and (minLat < pokemon['latitude'])
                        withinLong = (pokemon['longitude'] < maxLong) and (minLong < pokemon['longitude'])
                        if notInTheFuture and notTooOutDated and withinLong and withinLat:
                            spawnTime = spawnTime.strftime('%Y-%m-%d %H:%M:%S')
                            pokemonData = {'objId':pokemon['id'],
                             'created':str(spawnTime), 
                             'latitude':pokemon['latitude'], 
                             'longitude':pokemon['longitude'], 
                             'pokemonId':pokemon['pokemonId']}
                            if mode:
                                pokemonRequest = requests.post('http://127.0.0.1:8000/pokemon/?db=hunt',
                                data = pokemonData)
                            else:
                                pokemonRequest = requests.post('http://127.0.0.1:8000/pokemon/',
                                data = pokemonData)
                            if(rareTable[pokemon['pokemonId']] and pokemonRequest.content == pokemonNewlyFoundIdentifier) and withinEmailZone(pokemon):
                                sendEmail(accountData.me, accountData.pwd, accountData.me, str(pokemon['pokemonId']), pokemonDataToString(pokemonData))
                                print "Email Sended"
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        except:
            print "failed"
            print sys.exc_info()[0]
        print "small zone finished."
        nowMinLat += deltaLat
        if nowMinLat >= maxLat:
            nowMinLat = minLat
            print "cycle finished."
            #hunt mode
            if mode:
                time.sleep(60)
                pokemonRequest = requests.get('http://127.0.0.1:8000/pokemon/deleteOld/')
            else:
                time.sleep(300)
