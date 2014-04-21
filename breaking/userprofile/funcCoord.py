import math, random
from userprofile.models import UserProfile, MessageBox, Queue, GameInstance, Subcategory, Checkpoint

def generateCheckpointCoords(latitudeP, longitudeP):
    radius = random.uniform(0.002, 10*0.001)
    angle = random.randint(0,360)
    radians = math.radians(angle)
    latitude = math.sin(radians)*radius
    longitude = math.cos(radians)*radius
    latitude = latitude + float(latitudeP) 
    longitude = longitude + float(longitudeP)
    return latitude, longitude, radius

def generateCheckpointCoordsFromRadius(latitudeP, longitudeP, radius):
    angle = random.randint(0,360)
    radians = math.radians(angle)
    latitude = math.sin(radians)*radius
    longitude = math.cos(radians)*radius
    latitude = latitude + float(latitudeP) 
    longitude = longitude + float(longitudeP)
    return latitude, longitude

def checkCheckpointPositionByCoords(lati, longi, latP, longP):
    close = math.fabs(longi - float(longP)) + math.fabs(lati - float(latP))
    if(close > 0.0030):
        return True
    else:
        return False

def generateCheckpoint(player1, player2, gameInstance):
    latP1 = player1.latitude
    longP1 = player1.longitude
    latP2 = player2.latitude
    longP2 = player2.longitude
    while(True):
        tLatP1, tLongP1, radius = generateCheckpointCoords(latP1, longP1)
        isOK = checkCheckpointPositionByCoords(tLatP1, tLongP1, latP1, longP1)
        if isOK:
            tLatP2, tLongP2 = generateCheckpointCoordsFromRadius(latP2, longP2, radius)
            break
    return Checkpoint(game=gameInstance, latitudeP1=tLatP1, longitudeP1=tLongP1, latitudeP2=tLatP2, longitudeP2=tLongP2)
