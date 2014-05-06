from datetime import datetime, timedelta
import random

def offsetTime(timeStart1, timeEnd1, timeStart2, timeEnd2):
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