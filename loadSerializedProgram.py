import pickle
import datetime
from pprint import pprint

with open('program_obj.pickl', 'rb') as f:
    obj = pickle.load(f)




# normalize time
for key, value in obj.items():
    oldValue = value
    if len(value[0]) == 7:
        oldValue[0] = '0' + oldValue[0]
        obj[key] = oldValue
#pprint(obj)

timetable = {}
for key, value in obj.items():
    oldValue = value
    tempHour = int(value[0][0:2])
    if (value[0][6:8] == 'pm'):
        tempHour = int(value[0][0:2]) + 12       
        #print(int(oldValue[0][0:2]) + 12)
    #print(tempHour)
    newValue = [tempHour, value[1], value[2]]
    timetable[key] = newValue
pprint(timetable)
    

# create graph
graph = {}
for key, value in timetable.items():
    nodeList = []
    for key2, value2 in timetable.items():
        if (value[0] + 2 < value2[0] and value[0] + 5 > value2[0]):
            nodeList.append(key2)
    graph[key] = nodeList
pprint(graph)


'''
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
'''