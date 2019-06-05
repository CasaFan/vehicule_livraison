import numpy as np
import random


class test:
    def __init__(self):
        self.mDistances = np.loadtxt('/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/distances.txt')
        self.mTimes = np.loadtxt('/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/times.txt')
        self.demandesFile = open("/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/demandes.txt", "r")
        self.coordsFile = open("/Users/guelmortis/Documents/M2 MIAGE/vehicule_livraison/data/lyon1/coords.txt", "r")

        self.max_dist = 250
        self.capacity = 100
        self.charge_fast = 60
        self.charge_midium = 180
        self.charge_slow = 480
        self.start_time = "7:00"
        self.end_time = "19:00"
        self.totalDist = 0
        self.totalCapacity = 0
        self.totalTime = 0
        self.allTrucksTime = 0
        self.nbRetoursBase = 0
        self.indicesClients = 0
        self.lastDemande = 0
        self.j = 0
        self.newVehicle = False
        self.trajets = []
        self.solutions = []

        self.allTrucksDist = 0
        self.numV = 0
        self.rez = 0
        self.s = []
        self.sol = []
        self.k = 0
        self.func_index = 0
        self.best_score = 0
        self.best_route = []
        self.list_solution = []

        self.deliveryTime = 310

        # Ici récup par rapport au ini pour déclarer
        self.startTime = 7 * 3600
        self.endTime = 19 * 3600

        with self.demandesFile as df:
            line = df.readline()
            cnt = 1
            self.demandes = []
            while line:
                self.demandes.insert(cnt, line.rstrip('\n'))
                line = df.readline()
                cnt += 1

        with self.coordsFile as cf:
            line = cf.readline()
            cnt = 1
            self.coords = []
            while line:
                lineNoN = line.rstrip('\n')
                coord = lineNoN.split(",")
                self.coords.append(coord)
                line = cf.readline()
                cnt += 1

    # Cette methode va nous permettre de recuperer l'index des elements dans l'ordre original
    # Ce qui va nous permettre de travailler sur le meme jeu de donnees sans avoir a le modifier
    # Lorsque nous allons travailler sur les voisinages
    def get_index_list(self, list):
        i = 0
        result = []
        for l in list:
            result.append(i)
            i = i + 1
        # random.shuffle(result)
        result.append(len(list))
        result.append(-1)
        return result

    def get_index_list_for_solution(self, arrayList):
        array = [len(arrayList), -1]
        result = arrayList + array
        return result

    # Ce voisinage est le swap d'une valeur avec la valeur qui la suit
    def premier_voisinage(self, range, list):
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
    def deuxieme_voisinage(self, range, list):
        if range != -1:
            if range < (len(list)-2)/2:
                a, b = list[range], list[len(list)-3 - range]
                list[b], list[a] = list[a], list[b]
        return list
    
    # TODO A modifier pour recueprer un pourcentage des donnees
    # Remplacer 30% elements consecutifs par par 5 valeurs opposees
    def troisieme_voisinage(self, range, list):
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
    
    
    def check_if_demande_fits(self):
        for l in range(self.lastDemande, len(self.demandes)):
            if float(self.demandes[l]) + self.totalCapacity <= self.capacity:
                return l
        return False
    
    
    def respects_time_capacity_distance_constraints(self):
        return (((self.totalDist + float(self.mDistances[self.lastDemande][self.j]) + float(self.mDistances[len(self.demandes)][self.j])) <= self.max_dist)
                        and ((self.totalCapacity + float(self.demandes[self.lastDemande])) <= self.capacity)
                        and ((self.totalTime + self.mTimes[self.lastDemande][self.j] + self.deliveryTime) <= self.endTime))
    
    
    def respects_time_distance_constraints(self):
        return (((self.totalDist + float(self.mDistances[self.lastDemande][self.j]) + float(
            self.mDistances[len(self.demandes)][self.j])) <= self.max_dist)
        and ((self.totalTime + self.mTimes[self.lastDemande][self.j] + self.deliveryTime) <= self.endTime))
    
    
    def after_vehicule_recharge_still_time_left(self):
        return ((self.totalTime + (self.mTimes[len(self.demandes)][self.j]) * 2 + 3600) <= self.endTime)

    def initialize_heuristic_by_voisinage_order(self, func_index, i):
        if func_index == 1:
            return self.get_index_list(self.demandes)
        if func_index == 2:
            return self.premier_voisinage(i, self.get_index_list_for_solution(self.list_solution))
        if func_index == 3:
            return self.deuxieme_voisinage(i, self.get_index_list_for_solution(self.list_solution))
        if func_index == 4:
            return self.troisieme_voisinage(i, self.get_index_list_for_solution(self.list_solution))

    def export_file(self, file_name):
        with open(file_name, 'wb') as f:
            for b in self.best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'R', array)
                array2 = np.delete(array1, -1)
                array3 = np.delete(array2, 0)
                mat = np.asmatrix(array3)
                np.savetxt(f, mat, fmt='%s', delimiter=', ')

    def get_last_solution_as_list(self, route):
        flat_list = []
        for sublist in route:
            for item in sublist:
                flat_list.append(item)
        i = 0
        while i < len(flat_list):
            if flat_list[i] == -1:
                flat_list.remove(flat_list[i])
                # as an element is removed
                # so decrease the length by 1
                length = len(flat_list) - 1
                # run loop again to check element
                # at same index, when item removed
                # next item will shift to the left
                continue
            i = i + 1
        return flat_list
    
    
    def export_solution_depending_on_algo_case(self, index):
        if index == 1:
            self.export_file('sol.txt')
        # On export la meilleur solution dans un fichier txt
        if index == 2:
            self.export_file('sol_voisinage1.txt')
        if index == 3:
            self.export_file('sol_voisinage2.txt')
        if index == 4:
            self.export_file('sol_voisinage3.txt')
    
    # We chose to create an heuristic that puts chooses the client in the normal order, however when the next order
    # is too much to take, we check the remaining order to find one that can be added instead.
    # If we can we put it else we send it in the next trip
    def execute_heuristic(self):
        for func_index in range(1, 5):
            for client_index in range(-1, len(self.demandes)):
                client_list_by_index = self.initialize_heuristic_by_voisinage_order(func_index, client_index)

                # initialise variables for a new run of the algorithm. As such we need to initialise the different list
                # of elements of the heuristic such as the client list in the solution but also a list of their coordinates.
                # We use a dictionary for the solution with one attribute being the vehicle number and the other the trip
                # it will have to make that day
                self.j = client_list_by_index[0]
                k = 1
                self.newVehicle = True
                self.lastDemande = -1
                self.indicesClients = []
                self.trajets = []
                self.solutions = []
                self.sol = []
                # We also initialise the variables needed to compute the score
                self.allTrucksDist = 0
                self.allTrucksTime = 0
                self.numV = 0
                i = 1
                self.nbRetoursBase = 0
                self.rez = False
                removed = False
    
                while True:
                    # Initialise new vehicle with new time and self.solutions and capacity
                    if self.newVehicle:
                        self.numV += 1
                        self.totalDist = 0
                        self.totalCapacity = 0
                        self.totalTime = self.startTime
                        coordonees = []
                        solution = {}
                        trajet = {}
                        solution["vehicule"] = self.numV
                        trajet["vehicule"] = self.numV
                        coordonees.append(self.coords[len(self.demandes)])
    
                    if self.respects_time_capacity_distance_constraints():
                        if self.j in self.sol:
                            self.lastDemande = self.j
                            self.j = client_list_by_index[k]
                            k += 1
                        else:
                            coordonees.append(self.coords[self.j])
                            self.indicesClients.append(self.lastDemande)
                            # Add the constraints for the new delivery
                            self.totalDist += float(self.mDistances[self.lastDemande][self.j])
                            self.totalCapacity += float(self.demandes[self.lastDemande])
                            self.totalTime += self.mTimes[self.lastDemande][self.j] + self.deliveryTime
                            self.allTrucksTime += self.mTimes[self.lastDemande][self.j] + self.deliveryTime
                            self.newVehicle = False
                            self.lastDemande = self.j
                            self.j = client_list_by_index[k]
                            k += 1
    
                    else:
                        self.rez = self.check_if_demande_fits()
                        if self.rez != 0 and self.respects_time_distance_constraints():
                            self.sol.append(self.rez)
                            coordonees.append(self.coords[self.rez])
                            self.indicesClients.append(self.rez)
                            self.totalDist += float(self.mDistances[self.lastDemande][self.rez])
                            self.totalCapacity += float(self.demandes[self.lastDemande])
                            self.totalTime += self.mTimes[self.lastDemande][self.rez] + self.deliveryTime
                            self.allTrucksTime += self.mTimes[self.lastDemande][self.rez] + self.deliveryTime
                        else:
                            self.totalDist += float(self.mDistances[self.lastDemande][len(self.demandes)])
                            self.totalTime += self.mTimes[self.lastDemande][len(self.demandes)]
                            self.allTrucksTime += self.mTimes[self.lastDemande][len(self.demandes)]
                            self.allTrucksDist += self.totalDist
    
                        if self.after_vehicule_recharge_still_time_left():
                            coordonees.append(self.coords[len(self.demandes)])
                            # Vehicle returned to base and is preparing to be sent out again
                            # As such we recharge it (adding the charging time) and reset its total distance and capacity
                            self.totalDist = 0
                            self.totalCapacity = 0
                            self.totalTime += 3600
                            self.allTrucksTime += 3600
                            self.nbRetoursBase += 1
                            self.indicesClients.append(-1)
    
                        else:
                            coordonees.append(self.coords[len(self.demandes)])
                            trajet["coordonees"] = coordonees
                            self.trajets.append(trajet)
                            self.indicesClients.append(-1)
                            solution["indicesClients"] = self.indicesClients
                            self.solutions.append(solution)
                            self.indicesClients = [-1]
                            self.newVehicle = True
    
                    if k - 1 > len(self.demandes):
                        self.allTrucksDist += self.totalDist
                        trajet["coordonees"] = coordonees
                        self.trajets.append(trajet)
                        self.indicesClients.append(-1)
                        solution["indicesClients"] = self.indicesClients
                        self.solutions.append(solution)
                        self.indicesClients = [-1]
                        break
    
                score = self.allTrucksDist + (self.allTrucksTime/600) + (len(self.trajets)-1)*500
                print(self.list_solution)

                # On verifie si le score de cette solution est meilleur que la meilleure solution trouvee
                # On remplace l'acienne par celle-ci si elle est meilleure
                if self.best_score == 0:
                    self.best_score = score
                    for s in self.solutions:
                        self.best_route.append(s['indicesClients'])
                if self.best_score > score:
                    print('score', score)
                    self.best_score = score
                    self.best_route = []
                    for s in self.solutions:
                        self.best_route.append(s['indicesClients'])
    
            flat_list = self.get_last_solution_as_list(self.best_route)
            self.list_solution = flat_list
            self.export_solution_depending_on_algo_case(func_index)


test = test()
test.execute_heuristic()
