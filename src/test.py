"""
premier heuristique (intégré dans GUI)
"""

import numpy as np
import random

mDistances = np.loadtxt('/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/distances.txt')
mTimes = np.loadtxt('/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/times.txt')
demandesFile = open("/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/demandes.txt", "r")
coordsFile = open("/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/coords.txt", "r")


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

global totalDist
global totalCapacity
global totalTime
global allTrucksTime
global nbRetoursBase
global indicesClients
global lastDemande
global j
global newVehicle
global trajets
global solutions

global allTrucksDist
global numV
global i
global rez


# Cette methode va nous permettre de recuperer l'index des elements dans l'ordre original
# Ce qui va nous permettre de travailler sur le meme jeu de donnees sans avoir a le modifier
# Lorsque nous allons travailler sur les voisinages
def get_index_list(list):
    i = 0
    result = []
    for l in list:
        result.append(i)
        i = i + 1
    # random.shuffle(result)
    result.append(len(list))
    result.append(-1)
    return result


def get_index_list_for_solution(arrayList):
    array = [len(arrayList), -1]
    result = arrayList + array
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


# TODO A modifier pour recueprer un pourcentage des donnees
# Remplacer 30% elements consecutifs par par 5 valeurs opposees
def troisieme_voisinage(range, list):
    print(list)
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


def check_if_demande_fits(lastDemande, list, currentCapa, maxCapacity):
    for l in range(lastDemande, len(list)):
        if float(list[l]) + currentCapa <= maxCapacity:
            return l

    return False


def respects_time_capacity_distance_constraints():
    return (((totalDist + float(mDistances[lastDemande][j]) + float(mDistances[len(demandes)][j])) <= max_dist)
                    and ((totalCapacity + float(demandes[lastDemande])) <= capacity)
                    and ((totalTime + mTimes[lastDemande][j] + deliveryTime) <= endTime))


def respects_time_distance_constraints():
    return (((totalDist + float(mDistances[lastDemande][j]) + float(
        mDistances[len(demandes)][j])) <= max_dist)
    and ((totalTime + mTimes[lastDemande][j] + deliveryTime) <= endTime))


def after_vehicule_recharge_still_time_left():
    return ((totalTime + (mTimes[len(demandes)][j]) * 2 + 3600) <= endTime)


test = []
s0 = []
s1 = []
s2 = []

for func_index in range(1, 5):
    for i in range(-1, len(demandes)):
        if func_index == 1:
            test = get_index_list(demandes)
        if func_index == 2:
            test = premier_voisinage(i, get_index_list_for_solution(s0))
        if func_index == 3:
            test = deuxieme_voisinage(i, get_index_list_for_solution(s1))
        if func_index == 4:
            test = troisieme_voisinage(i, get_index_list_for_solution(s2))
        j = test[0]
        k = 1

        newVehicle = True
        lastDemande = -1
        indicesClients = []
        trajets = []
        solutions = []
        sol = []
        allTrucksDist = 0
        allTrucksTime = 0
        numV = 0
        i = 1
        nbRetoursBase = 0
        rez = False
        removed = False

        while True:
            # Initialise new vehicule with new time and solutions and capacity
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

            if respects_time_capacity_distance_constraints():
                coordonees.append(coords[j])
                indicesClients.append(lastDemande)
                # Add the constraints for the new delivery
                totalDist += float(mDistances[lastDemande][j])
                totalCapacity += float(demandes[lastDemande])
                totalTime += mTimes[lastDemande][j] + deliveryTime
                allTrucksTime += mTimes[lastDemande][j] + deliveryTime
                newVehicle = False
                lastDemande = j
                j = test[k]
                k += 1
                if lastDemande in sol:
                    lastDemande = j
                    j = test[k]
                    k += 1

            else:
                rez = check_if_demande_fits(lastDemande, demandes, totalCapacity, capacity)
                if rez != 0 and respects_time_distance_constraints():
                    sol.append(rez)
                    coordonees.append(coords[rez])
                    indicesClients.append(rez)
                    totalDist += float(mDistances[lastDemande][rez])
                    totalCapacity += float(demandes[lastDemande])
                    totalTime += mTimes[lastDemande][rez] + deliveryTime
                    allTrucksTime += mTimes[lastDemande][rez] + deliveryTime
                    rez = False
                else:
                    totalDist += float(mDistances[lastDemande][len(demandes)])
                    totalTime += mTimes[lastDemande][len(demandes)]
                    allTrucksTime += mTimes[lastDemande][len(demandes)]
                    allTrucksDist += totalDist

                if after_vehicule_recharge_still_time_left():
                    coordonees.append(coords[len(demandes)])
                    # Vehicule returned to base and is preparing to be sent out again
                    # As such we recharge it (adding the charging time) and reset its total distance and capacity
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

            if k - 1 > len(demandes):
                allTrucksDist += totalDist
                trajet["coordonees"] = coordonees
                trajets.append(trajet)
                solutions.append(solution)
                indicesClients.append(-1)
                solution["indicesClients"] = indicesClients
                indicesClients = [-1]
                break

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

    flat_list = []
    for sublist in best_route:
        for item in sublist:
            flat_list.append(item)

    while (i < len(flat_list)):
        if (flat_list[i] == -1):
            flat_list.remove(flat_list[i])
            # as an element is removed
            # so decrease the length by 1
            length = len(flat_list) - 1
            # run loop again to check element
            # at same index, when item removed
            # next item will shift to the left
            continue
        i = i + 1
    flat_list.remove(-1)

    if func_index == 1:
        s0 = flat_list
    if func_index == 2:
        s1 = flat_list
    if func_index == 3:
        s2 = flat_list


    def export_file(file_name):
        with open(file_name, 'wb') as f:
            for b in best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'R', array)
                array2 = np.delete(array1, -1)
                array3 = np.delete(array2, 0)
                mat = np.asmatrix(array3)
                np.savetxt(f, mat, fmt='%s', delimiter=', ')

    if func_index == 1:
        export_file('sol.txt')
    # On export la meilleur solution dans un fichier txt
    if func_index == 2:
        export_file('sol_voisinage1.txt')
    if func_index == 3:
        export_file('sol_voisinage2.txt')
    if func_index == 4:
        export_file('sol_voisinage3.txt')
