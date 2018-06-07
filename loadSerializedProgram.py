import pickle
import datetime
from pprint import pprint

with open('program_obj.pickl', 'rb') as f:
    obj = pickle.load(f)

tempKey = ""
tempValue = []
tempMark = 0

scheduleAM = {}
schedulePM = {}
schedule = {}

# normalize time
for key, value in obj.items():
    oldValue = value
    if len(value[0]) == 7:
        oldValue[0] = '0' + oldValue[0]
        obj[key] = oldValue

# divide noon
for key, value in obj.items():
    if 'am' in value[0]:
        scheduleAM[key] =  value
    if 'pm' in value[0]:
        schedulePM[key] =  value

# AM schedule
hour = 0
while (hour <= 10):
    for key, value in scheduleAM.items():
        if value[2] > tempMark and int(value[0][0:2]) > hour and int(value[0][0:2]) < hour+2:
            tempKey = key
            tempValue = value
            tempMark = value[2]
    if tempKey != "":            
        schedule[tempKey] = tempValue
    tempKey = ""
    tempValue = []
    tempMark = 0
    hour+=2
    
# PM schedule
hour = 0
while (hour <= 10):
    for key, value in schedulePM.items():
        if value[2] > tempMark and int(value[0][0:2]) > hour and int(value[0][0:2]) < hour+2:
            tempKey = key
            tempValue = value
            tempMark = value[2]
    if tempKey != "":
        schedule[tempKey] = tempValue
    tempKey = ""
    tempValue = []
    tempMark = 0
    hour+=2

# show schedule
for key, value in schedule.items():
    print(key,"         ", value)