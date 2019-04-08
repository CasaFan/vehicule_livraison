"""
premier heuristique (intégré dans GUI)
"""

import numpy as np


mDistances = np.loadtxt('/Users/guelmortis/Documents/MIAGE/vehicule_livraison/data/lyon1/distances.txt')
mTimes = np.loadtxt('/Users/guelmortis/Documents/MIAGE/vehicule_livraison/data/lyon1/times.txt')
demandesFile = open("/Users/guelmortis/Documents/MIAGE/vehicule_livraison/data/lyon1/demandes.txt", "r")
coordsFile = open("/Users/guelmortis/Documents/MIAGE/vehicule_livraison/data/lyon1/coords.txt", "r")


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
indicesDemande = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lastDemande = -1
indicesClients = []
trajets = []
solutions = []
j = 0
allTrucksDist = 0
allTrucksTime = 0
numV = 0
i = 1
nbRetoursBase = 0

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
        solution = {}
        trajet = {}
        solution["vehicule"] = numV
        trajet["vehicule"] = numV
        coordonees.append(coords[len(demandes)])

    if (
        ((totalDist + float(mDistances[lastDemande][j]) + float(mDistances[len(demandes)][j])) <= max_dist)
            and ((totalCapacity + float(demandes[lastDemande])) <= capacity)
            and ((totalTime + mTimes[lastDemande][j] + deliveryTime) <= endTime)
    ):
        coordonees.append(coords[j])
        indicesClients.append(lastDemande)
        totalDist += float(mDistances[lastDemande][j])
        totalCapacity += float(demandes[lastDemande])
        totalTime += mTimes[lastDemande][j] + deliveryTime
        allTrucksTime += mTimes[lastDemande][j] + deliveryTime
        newVehicle = False
        lastDemande = j
        j += 1

    else:
        totalDist += float(mDistances[lastDemande][len(demandes)])
        totalTime += mTimes[lastDemande][len(demandes)]
        allTrucksTime += mTimes[lastDemande][len(demandes)]
        allTrucksDist += totalDist

        if(totalTime + (mTimes[len(demandes)][j]) * 2 + 3600) <= endTime:
            coordonees.append(coords[len(demandes)])
            totalDist = 0
            totalCapacity = 0
            totalTime += 3600
            allTrucksTime += 3600
            nbRetoursBase += 1
            indicesClients.append(-1)

        else:
            coordonees.append(coords[len(demandes)])
            trajet["coordonees"] = coordonees
            trajets.append(trajet)
            solutions.append(solution)
            indicesClients.append(-1)
            solution["indicesClients"] = indicesClients
            indicesClients = [-1]
            newVehicle = True


coordonees.append(coords[len(demandes)])
indicesClients.append(-1)
trajet["coordonees"] = coordonees
solution["indicesClients"] = indicesClients
solutions.append(solution)
trajets.append(trajet)
allTrucksDist += totalDist

print(allTrucksDist)
print(allTrucksTime)
print(len(trajets))
score = allTrucksDist + (allTrucksTime/600) + (len(trajets)-1)*500
for i in trajets:
    print(i)

for i in solutions:
    print(i)
print('score:')
print(score)