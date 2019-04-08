"""
premier heuristique (intégré dans GUI)
"""

import numpy as np


mDistances = np.loadtxt('D:/Cours/M2 Miage/Energie/lyon0/distances.txt')
mTimes = np.loadtxt('D:/Cours/M2 Miage/Energie/lyon0/times.txt')
demandesFile = open("D:/Cours/M2 Miage/Energie/lyon0/demandes.txt", "r")
coordsFile = open("D:/Cours/M2 Miage/Energie/lyon0/coords.txt", "r")


max_dist = 250
capacity = 100
charge_fast = 60
charge_midium = 180
charge_slow = 480
start_time = "7:00"
end_time = "19:00"

deliveryTime = 310

#Ici récup par rapport au ini pour déclarer
startTime = 7*3600
endTime = 19*3600

with demandesFile as df:  
   line = df.readline()
   cnt = 1
   demandes = []
   while line:
       demandes.insert(cnt, line.rstrip('\n'))
       line = df.readline()
       cnt += 1

with coordsFile as cf:  
   line = cf.readline()
   cnt = 1
   coords = []
   while line:
       lineNoN = line.rstrip('\n')
       coord = lineNoN.split(",")       
       coords.append(coord)
       line = cf.readline()
       cnt += 1       

newVehicle = True
lastDemande = 0
trajets = []
allTrucksDist = 0
allTrucksTime = 0
numV = 0

"""
print('result: ')
print(mDistances)
print('[fin result]')
raise SystemError
"""
while lastDemande < len(demandes):

    if newVehicle:
        numV += 1
        totalDist = 0
        totalCapacity = 0
        totalTime = startTime
        coordonees = []
        trajet = {}
        trajet["vehicule"] = numV
        coordonees.append(coords[0])

    if (
        ((totalDist + float(mDistances[lastDemande][lastDemande+1]) + float(mDistances[0][lastDemande+1])) <= max_dist)
        and ((totalCapacity + float(demandes[lastDemande])) <= capacity)
        and ((totalTime + mTimes[lastDemande][lastDemande+1] + deliveryTime) <= endTime)
    ):
        coordonees.append(coords[lastDemande + 1])
        totalDist += float(mDistances[lastDemande][lastDemande+1])
        totalCapacity += float(demandes[lastDemande])
        totalTime += mTimes[lastDemande][lastDemande+1] + deliveryTime
        allTrucksTime += mTimes[lastDemande][lastDemande+1] + deliveryTime
        newVehicle = False
        lastDemande += 1

    else:
        totalDist += float(mDistances[lastDemande][0])
        totalTime += mTimes[lastDemande][0]
        allTrucksTime += mTimes[lastDemande][0]
        allTrucksDist += totalDist

        if(totalTime + (mTimes[0][lastDemande+1])*2 + 3600) <= endTime:
            coordonees.append(coords[0])
            totalDist = 0
            totalCapacity = 0
            totalTime += 3600
            allTrucksTime += 3600

        else:
            coordonees.append(coords[0])
            trajet["coordonees"] = coordonees
            trajets.append(trajet)
            newVehicle = True

coordonees.append(coords[0])
trajet["coordonees"] = coordonees
trajets.append(trajet)
allTrucksDist += totalDist

print(allTrucksDist)
print(allTrucksTime)
print(len(trajets))
score = allTrucksDist + (allTrucksTime/600) + (len(trajets)-1)*500
print(trajets)
print(score)