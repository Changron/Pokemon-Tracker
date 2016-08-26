import requests
import datetime
from datetime import timedelta
import sys
import time
import smtplib
import account_data
from email.MIMEText import MIMEText
from user_list import user_list, tracker_list

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

def withinZone(pokemon, area):
    withinLat = (pokemon['latitude'] < area.max_lat) and (area.min_lat < pokemon['latitude'])
    withinLong = (pokemon['longitude'] < area.max_long) and (area.min_long < pokemon['longitude'])
    return withinLong and withinLat

def withinTime(spawn_time):
    now = datetime.datetime.now()
    notTooOutDated = (now - timedelta(minutes = 30) < spawn_time)
    notInTheFuture = (spawn_time - timedelta(minutes = 30) < now)
    return notTooOutDated and notInTheFuture

def userWantsEmail(user, pokemon, respond):
    isInUserTable = user.table[pokemon['pokemonId']]
    didNotSendEmailYet = (respond.content == pokemonNewlyFoundIdentifier)
    withinEmailZone = withinZone(pokemon, user.area)
    userIsActive = user.active
    return isInUserTable and didNotSendEmailYet and withinEmailZone and userIsActive

# mode 0, normal
# mode 1, hunting mode, only rare pokemon will be recorded
mode = 0

if __name__ == "__main__":
    mode = int(raw_input("Enter Mode: (0 for normal, 1 for hunting mode)"))

    delta_lat = 0.03
    search_list = user_list
    if mode == 0:
        search_list = tracker_list

    while True:
        for user in search_list:
            if (mode and user.active) or (mode == 0):
                now_min_lat = user.area.min_lat
                while now_min_lat < user.area.max_lat:
                    try:
                        res = getRequest(now_min_lat, min(user.area.max_lat, now_min_lat+delta_lat), user.area.min_long, user.area.max_long)
                        response = requests.get(res)
                        pokemons = response.json()
                        #for all pokemons
                        for pokemon in pokemons['data']:
                            # if pokemon is system detected
                            if pokemon['trainerName'] == systemDetectIdentifier:
                                # if the pokemon is the one we want to record
                                if user.table[pokemon['pokemonId']]:
                                    spawnTime = datetime.datetime.fromtimestamp(int(pokemon['created']))
                                    if withinTime(spawnTime) and withinZone(pokemon, user.area):
                                        spawnTime = spawnTime.strftime('%Y-%m-%d %H:%M:%S')
                                        pokemonData = {'objId':pokemon['id'],
                                         'created':str(spawnTime), 
                                         'latitude':pokemon['latitude'], 
                                         'longitude':pokemon['longitude'], 
                                         'pokemonId':pokemon['pokemonId']}
                                        if mode:
                                            pokemonRespond = requests.post('http://127.0.0.1:8000/pokemon/?db=hunt',
                                            data = pokemonData)
                                        else:
                                            pokemonRespond = requests.post('http://127.0.0.1:8000/pokemon/',
                                            data = pokemonData)
                                        # if user wants, if newly found, and is near enough
                                        if userWantsEmail(user, pokemonData, pokemonRespond):
                                            sendEmail(account_data.me, account_data.pwd, user.email, str(pokemon['pokemonId']), pokemonDataToString(pokemonData))
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
                    now_min_lat += delta_lat
                    if now_min_lat >= user.area.max_lat:
                        print "cycle finished."
                        #hunt mode
            else:
                pass
        if mode:
            time.sleep(60)
        else:
            time.sleep(300)
