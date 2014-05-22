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


def generateCheckpointClosePlayer(player1, player2, gameInstance):
    latP1 = player1.latitude
    longP1 = player1.longitude
    latP2 = player2.latitude
    longP2 = player2.longitude
    latCenter = (float(latP1)  + float(latP2)) / 2
    longCenter = (float(longP1)  + float(longP2)) / 2
    while(True):
        tLatCenter, tLongCenter, radius = generateCheckpointCoords(latCenter, longCenter)
        isOKP1 = checkCheckpointPositionByCoords(tLatCenter, tLatCenter, latP1, longP1)
        isOKP2 = checkCheckpointPositionByCoords(tLatCenter, tLatCenter, latP2, longP2)
        if isOKP1 and isOKP2:
            break
    return Checkpoint(game=gameInstance, latitudeP1=tLatCenter, longitudeP1=tLongCenter, latitudeP2=tLatCenter, longitudeP2=tLongCenter)
