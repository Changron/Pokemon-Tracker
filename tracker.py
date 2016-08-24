import requests
import datetime
import sys
import time


maxLat = 22.78
minLat = 22.47
deltaLat = 0.03

maxLong = 120.44
minLong = 120.245

systemDetectIdentifier = "(Poke Radar Prediction)"

def getRequest(minLatitude, maxLatitude, minLongitude, maxLongitude):
    url = "https://www.pokeradar.io/api/v1/submissions?deviceId=e75a51005d0e11e6a5118f01dbbb3e30&minLatitude=%s&maxLatitude=%s&minLongitude=%s&maxLongitude=%s&pokemonId=0" % (
        minLatitude, maxLatitude, minLongitude, maxLongitude)
    return url

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

if __name__ == "__main__":
    nowMinLat = minLat

    while True:
        try:
            res = getRequest(nowMinLat, min(maxLat, nowMinLat+deltaLat), minLong, maxLong)
            response = requests.get(res)
            pokemons = response.json()
            for pokemon in pokemons['data']:
                if pokemon['trainerName'] == systemDetectIdentifier:
                    if table[pokemon['pokemonId']]:
                        spawnTime = datetime.datetime.fromtimestamp(int(pokemon['created'])).strftime('%Y-%m-%d %H:%M:%S')
                        pokemonRequest = requests.post('http://127.0.0.1:8000/pokemon/',
                         data = {'objId':pokemon['id'],
                         'created':str(spawnTime), 
                         'latitude':pokemon['latitude'], 
                         'longitude':pokemon['longitude'], 
                         'pokemonId':pokemon['pokemonId']})
                    else:
                        pass
                else:
                    pass
        except:
            print "failed"
            print sys.exc_info()[0]
        print "finished"
        nowMinLat += deltaLat
        if nowMinLat >= maxLat:
            nowMinLat = minLat
            time.sleep(300)
