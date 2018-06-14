import pickle
import datetime
from pprint import pprint

with open('program_obj.pickl', 'rb') as f:
    obj = pickle.load(f)


def find_path(graph, start, end, pathCost, path=[]):
        path = path + [start]     
        pathCost += timetable[start][2]
        print(pathCost)
        if start == end:
            return path
        if start not in graph:
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, pathCost, path)
                if newpath: 
                    
                    
                    return newpath
        return None


def find_all_paths(graph, start, end, pathCost, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, pathCost, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


def evaluate_paths(paths):
    bestPath = []
    bestMark = 0
    for path in paths:
        mark = 0
        for node in path:
            mark += timetable[node][2]
        if (bestMark < mark):
            bestMark = mark
            bestPath = path 
    return bestPath


# normalize time
for key, value in obj.items():
    oldValue = value
    if len(value[0]) == 7:
        oldValue[0] = '0' + oldValue[0]
        obj[key] = oldValue
pprint(obj)

timetable = {}
for key, value in obj.items():
    oldValue = value
    tempHour = int(value[0][0:2])
    if (value[0][6:8] == 'pm'):
        tempHour = int(value[0][0:2]) + 12
    newValue = [tempHour, value[1], value[2]]
    timetable[key] = newValue
    

# create graph
graph = {}
for key, value in timetable.items():
    nodeList = []
    for key2, value2 in timetable.items():
        if (value[0] + 2 < value2[0] and value[0] + 5 > value2[0]):
            nodeList.append(key2)
    graph[key] = nodeList

# firs and last
first = 24
firstMovie = ""
last = 0
lastMovie = ""
for key, value in timetable.items():
    if value[0] < first:
        first = value[0]
        firstMovie = key
    if value[0] > last:
        last = value[0]
        lastMovie = key



pathCost = 0

allPaths = find_all_paths(graph, firstMovie, lastMovie, pathCost)

bestPath = evaluate_paths(allPaths)

print("\n\n\n\n")

for film in bestPath:
    print(film,"     ", obj[film])
