"""
premier heuristique (intégré dans GUI)
"""

import numpy as np

mDistances = np.loadtxt('../data/lyon1/distances.txt')
mTimes = np.loadtxt('../data/lyon1/times.txt')
demandesFile = open("../data/lyon1/demandes.txt", "r")
coordsFile = open("../data/lyon1/coords.txt", "r")


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

best_score = 0
best_route = []


# Cette methode va nous permettre de recuperer l'index des elements dans l'ordre original
# Ce qui va nous permettre de travailler sur le meme jeu de donnees sans avoir a le modifier
# Lorsque nous allons travailler sur les voisinages
def get_index_list(list):
    i = 0
    result = []
    for l in list:
        result.append(i)
        i = i + 1
    result.append(len(list))
    result.append(-1)
    return result


# Ce voisinage est le swap d'une valeur avec la valeur qui la suit
def premier_voisinage(range, list):
    if range != -1:
        if range+1 < len(list) - 2:
            a, b = list[range], list[range+1]
            list[b], list[a] = list[a], list[b]
        else:
            a, b = list[0], list[range]
            list[b], list[a] = list[a], list[b]
    return list


# Ce voisinage est l'inversion d'une valeur et de son opposee dans la liste
# ex: dans une liste de 10 elements, on inverse 1 et 10 ou bien 2 et 9, etc.
def deuxieme_voisinage(range, list):
    if range != -1:
        if range < (len(list)-2)/2:
            a, b = list[range], list[len(list)-3 - range]
            list[b], list[a] = list[a], list[b]
    return list


# Remplacer 5 elements consecutifs par par 5 valeurs opposees
def troisieme_voisinage(range, list):
    if range != -1:
        if range < (len(list)-7)/2:
            a, b = list[range], list[len(list)-3 - range]
            list[b], list[a] = list[a], list[b]
            a, b = list[range+1], list[len(list) - 4 - range]
            list[b], list[a] = list[a], list[b]
            a, b = list[range+2], list[len(list) - 5 - range]
            list[b], list[a] = list[a], list[b]
            a, b = list[range+3], list[len(list) - 6 - range]
            list[b], list[a] = list[a], list[b]
            a, b = list[range+4], list[len(list) - 7 - range]
            list[b], list[a] = list[a], list[b]
    return list

"""
print('result: ')
print(mDistances)
print('[fin result]')
raise SystemError
"""

test = []

for func_index in range(1, 4):
    for i in range(-1, len(demandes)):
        if func_index == 1:
            test = premier_voisinage(i, get_index_list(demandes))
        if func_index == 2:
            test = deuxieme_voisinage(i, get_index_list(demandes))
        if func_index == 3:
            test = troisieme_voisinage(i, get_index_list(demandes))
        j = test[0]
        k = 1

        newVehicle = True
        lastDemande = -1
        indicesClients = []
        trajets = []
        solutions = []

        allTrucksDist = 0
        allTrucksTime = 0
        numV = 0
        i = 1
        nbRetoursBase = 0

        while k - 1 < len(demandes) and lastDemande != len(demandes):
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
                j = test[k]
                k += 1

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

        # On sort de la boucle avant de rajouter le dermier element, il faut donc faire une derniere fois
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
        else:
            totalDist += float(mDistances[lastDemande][len(demandes)])
            totalTime += mTimes[lastDemande][len(demandes)]
            allTrucksTime += mTimes[lastDemande][len(demandes)]
            allTrucksDist += totalDist

            if (totalTime + (mTimes[len(demandes)][j]) * 2 + 3600) <= endTime:
                coordonees.append(coords[len(demandes)])
                totalDist = 0
                totalCapacity = 0
                totalTime += 3600
                allTrucksTime += 3600
                nbRetoursBase += 1
                coordonees.append(coords[j])
                indicesClients.append(lastDemande)
                totalDist += float(mDistances[lastDemande][j])
                totalCapacity += float(demandes[lastDemande])
                totalTime += mTimes[lastDemande][j] + deliveryTime
                allTrucksTime += mTimes[lastDemande][j] + deliveryTime
                newVehicle = False

            else:
                coordonees.append(coords[len(demandes)])
                trajet["coordonees"] = coordonees
                trajets.append(trajet)
                solutions.append(solution)
                solution["indicesClients"] = indicesClients
                indicesClients = [-1]
                newVehicle = True

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

            coordonees.append(coords[j])
            indicesClients.append(lastDemande)
            totalDist += float(mDistances[lastDemande][j])
            totalCapacity += float(demandes[lastDemande])
            totalTime += mTimes[lastDemande][j] + deliveryTime
            allTrucksTime += mTimes[lastDemande][j] + deliveryTime
            newVehicle = False

        coordonees.append(coords[len(demandes)])
        indicesClients.append(-1)
        trajet["coordonees"] = coordonees
        solution["indicesClients"] = indicesClients
        solutions.append(solution)
        trajets.append(trajet)
        allTrucksDist += totalDist

        score = allTrucksDist + (allTrucksTime/600) + (len(trajets)-1)*500

        # On verifie si le score de cette solution est meilleur que la meilleure solution trouvee
        # On remplace l'acienne par celle-ci si elle est meilleure
        if best_score == 0:
            best_score = score
            for s in solutions:
                best_route.append(s['indicesClients'])
        if best_score > score:
            best_score = score
            best_route = []
            for s in solutions:
                best_route.append(s['indicesClients'])

        # for i in solutions:
        #     print(i)
        # print('score:')
        # print(score)

    print('The best score is:', best_score)
    print('solution', best_route)

    # On export la meilleur solution dans un fichier txt
    if func_index == 1:
        with open('sol_voisinage1.txt', 'wb') as f:
            for b in best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'C', array)
                mat = np.asmatrix(array1)
                np.savetxt(f, mat, fmt='%s')
    if func_index == 2:
        with open('sol_voisinage2.txt', 'wb') as f:
            for b in best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'C', array)
                mat = np.asmatrix(array1)
                np.savetxt(f, mat, fmt='%s')
    if func_index == 3:
        with open('sol_voisinage3.txt', 'wb') as f:
            for b in best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'C', array)
                mat = np.asmatrix(array1)
                np.savetxt(f, mat, fmt='%s')

