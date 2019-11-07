import sys
import json

json_data = {}

with open("cs.json") as json_file:
    json_data = json.load(json_file)

simulation_time = json_data["simulation"]["duration"]
links = json_data["links"]

occupied_by_s = {}
in_progress = []  # TODO: ami mar kesz azt kivenni


def getCircuit(json_data, start, end):
    ret = []
    for i in json_data['possible-circuits']:
        lastIndex = len(i) - 1
        if (i[0] == start and i[lastIndex] == end):
            return [i]


def append(target, item):
    for i in item:
        target.append(i)


def getPairs(arr):
    ret = []
    for i in range(0, len(arr), 2):
        x = i
        asd = arr[x:x+2]
        ret.append(arr[x:x+2])

    if len(arr) % 2 != 0:
        tmp = [arr[len(arr) - 2], arr[len(arr) - 1]]
        ret[len(ret) - 1] = tmp
    return ret


def checkCapacityAndRoute(arr, capacity):
    counter = 0
    for item in arr:
        for i in links:
            # bennevan es megfelelo kapacitasu a keres
            if (item == i["points"] and capacity <= i["capacity"]):
                counter += 1
    # ha mindegyik elemere passzol akkor ok
    return len(arr) == counter

n = json_data["simulation"]["duration"] + 1

for i in range(1,n):
    occupied_by_s[i] = []

for i in json_data["simulation"]["demands"]:
    for j in range(i['start-time'], i['end-time'] + 1):
        tmp = getCircuit(json_data, i['end-points'][0], i['end-points'][1])
        route = getPairs(tmp[0])
        if (checkCapacityAndRoute(route, i['demand']) == True):
            append(occupied_by_s[j], tmp)
        # else:
            # ahol nincs utvonal vagy kicsi a capacity azokat itt kell lekezelni
            # print("sikertelen", tmp, route)

def isInProgress(time):
    done = []
    for i in in_progress:
        if (occupied_by_s[time].count(i) == 0):
            done.append(i)

    for i in done:
        print("igény felszabadítás: ", i[0], "<->", i[-1], " st:", time - 1)
        in_progress.remove(i)


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return True
    return False

def removeFromOccupied(item, startTime):
	tmp = [item[0], item[len(item)-1]]
	for i in json_data["simulation"]["demands"]:
		if (i['end-points'] == tmp and i['start-time'] == startTime):
			endTime = i['end-time']
	
	for i in occupied_by_s:
		if (i == startTime):
			occupied_by_s[i].remove(item)
			startTime += 1
		if (i == endTime):
			break
		
	


def checkIfInprogress(obj, time):
    # igeny felszabaditas
    isInProgress(time)
    tmp = []
    asd = False
    for item in obj:
        # ha uj
        if (in_progress.count(item) == 0):
            # ellenorizni, hogy nincs-e utkozes
            for i in in_progress:
                tmp = item[1:-1]
                asd = common_member(i, tmp)
            if (asd == True):
                dasqdw = 12
                removeFromOccupied(item, time)
                print("igény foglalás: ", item[0], "<->", item[-1], " st:", time," – sikertelen")
            else:
                print("igény foglalás: ", item[0], "<->", item[-1], " st:", time," – sikeres")
                in_progress.append(item)
        # else:
        #     print("Bennevan es meg fut")


for t in occupied_by_s:
    checkIfInprogress(occupied_by_s[t], t)