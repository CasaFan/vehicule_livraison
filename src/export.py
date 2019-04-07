"""
premier heuristique (intégré dans GUI)
"""

import numpy as np


mDistances = np.loadtxt('C:/Users/gs63vr/PycharmProjects/energy/data/lyon1/distances.txt')
mTimes = np.loadtxt('C:/Users/gs63vr/PycharmProjects/energy/data/lyon1/times.txt')
demandesFile = open("C:/Users/gs63vr/PycharmProjects/energy/data/lyon1/demandes.txt", "r")
coordsFile = open("C:/Users/gs63vr/PycharmProjects/energy/data/lyon1/coords.txt", "r")


max_dist = 250
capacity = 100
charge_fast = 60
charge_midium = 180
charge_slow = 480
start_time = "7:00"
end_time = "19:00"

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

"""
print('result: ')
print(mDistances)
print('[fin result]')
raise SystemError
"""
while lastDemande < len(demandes):

    if newVehicle:
        totalDist = 0
        totalCapacity = 0
        totalTime = startTime
        trajet = []
        trajet.append(coords[0])
    if ((totalDist + int(mDistances[lastDemande][lastDemande+1]) + int(mDistances[0][lastDemande+1])) <= max_dist) and ((totalCapacity + int(demandes[lastDemande])) <= capacity) and ((totalTime + mTimes[lastDemande][lastDemande+1]) <= endTime):
        trajet.append(coords[lastDemande + 1])
        totalDist += int(mDistances[lastDemande][lastDemande+1])
        totalCapacity += int(demandes[lastDemande])
        totalTime += mTimes[lastDemande][lastDemande+1] 
        newVehicle = False
        lastDemande += 1
    else:
        newVehicle = True
        trajets.append(trajet)

trajets.append(trajet)
    
for t in trajets:
    print(t) 
    print('\n')