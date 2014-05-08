from datetime import datetime, timedelta
import random

def offsetTime(timeStart1, timeEnd1, timeStart2, timeEnd2):
	if(timeStart1 <= 1 and timeStart1 >=23):
		timeStart1 = 16;
	if(timeEnd1 <= 1 and timeEnd1 >=23):
		timeEnd1 = 21;
	if(timeStart2 <= 1 and timeStart2 >=23):
		timeStart2 = 16;
	if(timeEnd1 <= 1 and timeEnd1 >=23):
		timeEnd1 = 21;

	if timeStart1 > timeStart2:
		beginTime = timeStart1
	else:
		beginTime = timeStart2

	if timeEnd1 < timeEnd2:
		endTime = timeEnd1
	else:
		endTime = timeEnd2

	now = datetime.now()
	hTime = random.randint(int(beginTime), int(endTime) - 1)
	mTime = random.randint(1, 59)
	h = 23 - now.hour
	m = 60 - now.minute
	h = h + hTime
	m = m + mTime
	dtWithOffset = now + timedelta(hours=h,minutes=m)
	return dtWithOffset

def makeGameInstance(playerQ1, player2, gameMode):
	whenGenerateCheckpoints = offsetTime(
		playerQ1.timeStart,
		playerQ1.timeEnd,
		player2.timeStart,
		player2.timeEnd)#moment w ktorym checkpointy powinny zostac udostępnione przez Webservice
    gInstance = GameInstance(
     	player1=player1,
     	player2=player2,
     	dateTime1=datetime.datetime.now(),
     	dateTime2=whenGenerateCheckpoints,
     	available=True,
     	mode=gameMode)
    gInstance.save()
    checkpoint = generateCheckpoint(playerQ1, player2, gInstance)
    checkpoint.save()
    playerQ1.delete()