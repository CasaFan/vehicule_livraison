import numpy as np
import random


class Heuristic:

    def __init__(self, data_set, vehicule_config):
        self.mDistances = data_set['distances']
        self.mTimes = data_set['times']
        self.demandes = data_set['demands']
        self.coords = data_set['coordinates']

        self.max_dist = vehicule_config.max_dist
        self.capacity = vehicule_config.capacity
        self.charge_fast = vehicule_config.charge_fast * 60
        self.charge_midium = vehicule_config.charge_midium * 60
        self.charge_slow = vehicule_config.charge_slow * 60
        self.startTime = vehicule_config.start_time
        self.endTime = vehicule_config.end_time

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
        self.func_index = 1
        self.client_index = -1
        self.allTrucksDist = 0
        self.numV = 0
        self.adding_another_client = 0
        self.s = []
        self.sol = []
        self.k = 0
        self.best_score = 0
        self.best_route = []
        self.list_solution = []

    # Cette methode va nous permettre de recuperer l'index des elements dans l'ordre original
    # Ce qui va nous permettre de travailler sur le meme jeu de donnees sans avoir a le modifier
    # Lorsque nous allons travailler sur les voisinages
    def get_index_list(self, list, choice):
        """
        Cette methode va nous permettre de recuperer l'index des elements dans l'ordre original
        Ce qui va nous permettre de travailler sur le meme jeu de donnees sans avoir a le modifier
        Lorsque nous allons travailler sur les voisinages
        :param list:
        :param choice:
        :return: result
        """
        i = 0
        result = []
        for l in list:
            result.append(i)
            i = i + 1

        """ 
        On selectionne aleatoirement les element de notre liste pour avoir des resultats 
        Non deterministes de notre heuristique
        """
        if choice == 2 or choice == 4:
            random.shuffle(result)
        result.append(len(list))
        result.append(-1)
        return result

    def get_index_list_for_solution(self, arrayList):
        """
        Le format des donnees des solutions est different de l'initial
        et donc pour chaque voisinage, on utilise cette methode qui recupere nos id clients
        et qui rajoute la longueur de la liste et -1 (le premier pour est pour qu'on parcours
        bien tous nos clients et le second represente l'entrepot
        :param arrayList:
        :return: result:
        """
        array = [len(arrayList), -1]
        result = arrayList + array
        return result

    def premier_voisinage(self, range, list):
        """
        Question 1 : Ce voisinage est le swap d'une valeur avec la valeur qui la suit
        Dans tous ces cas, on ne gere pas le cas ou la liste est vide.
        Dans notre facon de penser, on a suppose que si l'entreprise n'avait
        pas de client, qu'elle n'ait donc pas besoin de l'outil
        :param range:
        :param list:
        :return: list:
        """
        if range != -1:
            if range+1 < len(list) - 2:
                a, b = list[range], list[range+1]
                list[b], list[a] = list[a], list[b]
            else:
                a, b = list[0], list[range]
                list[b], list[a] = list[a], list[b]
        return list

    def delivery_time(self):
        """
        Calcule le temps que prend une livraison 5min + 10 secondes par collis
        :return:
        """
        return (300 + 10 * float(self.demandes[self.lastDemande]))

    def deuxieme_voisinage(self, range, list):
        """
        Question 1: Ce voisinage est l'inversion d'une valeur et de son opposee dans la liste
        ex: dans une liste de 10 elements, on inverse 1 et 10 ou bien 2 et 9, etc.
        :param range:
        :param list:
        :return: list:
        """
        if range != -1:
            if range < (len(list)-2)/2:
                a, b = list[range], list[len(list)-3 - range]
                list[b], list[a] = list[a], list[b]
        return list

    def troisieme_voisinage(self, my_range, my_list):
        """
        Question 1: Remplacer 30% elements consecutifs par leur 30% opposes
        :param my_range:
        :param my_list:
        :return: my_list
        """
        if my_range != -1:
            my_percent = round(len(my_list) * 30 / 100)
            if my_range < (round(len(my_list) / 2) - my_percent):
                my_switch_list = list(range(my_percent))
                for my_switch in my_switch_list:
                    my_list[my_range + my_switch], my_list[len(my_list) - 3 - (my_range + my_switch)] = \
                        my_list[len(my_list) - 3 - (my_range + my_switch)], my_list[my_range + my_switch]
        return my_list
    
    def check_if_demande_fits(self):
        """
        Verfier dans le reste de notre liste de clients, il exsite une demande que l'on peut ajouter
        dans le vehicule si oui, c'est la valeur qu'on renvoie, sinon on renvoie faux
        :return:
        """
        for l in range(self.lastDemande, len(self.demandes)):
            if float(self.demandes[l]) + self.totalCapacity <= self.capacity:
                return l
        return False
    
    def respects_time_capacity_distance_constraints(self):
        """
        Verifie si l'on depasse pas la capacite no le temps ni la distance
        On a decide de mettre des contraintes inviolables dans notre cas
        :return: True or False
        """
        return (((self.totalDist + float(self.mDistances[self.lastDemande][self.j]) + float(self.mDistances[len(self.demandes)][self.j])) <= self.max_dist)
                        and ((self.totalCapacity + float(self.demandes[self.lastDemande])) <= self.capacity)
                        and ((self.totalTime + self.mTimes[self.lastDemande][self.j] + self.delivery_time()) <= self.endTime))
    
    
    def respects_time_distance_constraints(self):
        """
        Meme que precedement mais cette fois selement pour le temps et la distance
        :return:
        """
        return (((self.totalDist + float(self.mDistances[self.adding_another_client][self.j]) + float(
            self.mDistances[len(self.demandes)][self.j])) <= self.max_dist)
        and ((self.totalTime + self.mTimes[self.adding_another_client][self.j] + self.delivery_time()) <= self.endTime))
    
    
    def after_vehicule_recharge_still_time_left(self):
        """
        On verifie si meme apres une recharge du vehicule, il nous reste tout de meme
        du temps pour un dernier voyage
        :return:
        """
        return ((self.totalTime + (self.mTimes[len(self.demandes)][self.j]) * 2 + 3600) <= self.endTime)

    def initialize_heuristic_by_voisinage_order(self, i, choice):
        """
        Ici on initialise notre jeu de donne, tout d'abord en recuperant l'indice client
        par la liste des demandes. Dans un deuxieme cas, la solution recuperee par notre
        algo sera lancee modifee avec le voisinage 1 pour etre traitee. Puis 2 et 3..
        :param i:
        :param choice:
        :return:
        """
        if self.func_index == 1:
            return self.get_index_list(self.demandes, choice)
        if self.func_index == 2:
            return self.premier_voisinage(i, self.get_index_list_for_solution(self.list_solution))
        if self.func_index == 3:
            return self.deuxieme_voisinage(i, self.get_index_list_for_solution(self.list_solution))
        if self.func_index == 4:
            return self.troisieme_voisinage(i, self.get_index_list_for_solution(self.list_solution))

    def export_file(self, file_name):
        """
        Exporter la solution dans un fichier tout en transformant les -1 que nous avons
        dedans en R pour recharge. Nous supposons qu'a chaque retour au depot on recharge
        :param file_name:
        :return:
        """
        with open(file_name, 'wb') as f:
            for b in self.best_route:
                array = np.asarray(b)
                array1 = np.where(array == -1, 'R', array)
                array2 = np.delete(array1, -1)
                array3 = np.delete(array2, 0)
                mat = np.asmatrix(array3)
                np.savetxt(f, mat, fmt='%s', delimiter=', ')

    def get_last_solution_as_list(self, route):
        """
        Transformer la derniere solution obtenue en une liste manipulable d'id clients
        :param route:
        :return:
        """
        result_list = []
        for sous_list in route:
            for item in sous_list:
                result_list.append(item)
        i = 0
        while i < len(result_list):
            if result_list[i] == -1:
                result_list.remove(result_list[i])
                length = len(result_list) - 1
                continue
            i = i + 1
        return result_list

    def export_solution_depending_on_algo_case(self, index):
        """
        Nous permet d'exporter pour chacune des iteration de notre algo
        un fichier qui contiendra la meilleur solution pour chacun des voisinage
        :param index:
        :return:
        """
        if index == 1:
            self.export_file('sol.txt')
        # On export la meilleur solution dans un fichier txt
        if index == 2:
            self.export_file('sol_voisinage1.txt')
        if index == 3:
            self.export_file('sol_voisinage2.txt')
        if index == 4:
            self.export_file('sol_voisinage3.txt')
    
    def best_score_solution(self):
        """
        Calcul du score et comparaison avec le meilleur score courant
        Si meilleur, le remplace sinon garde l'ancien et enfin on export le resultat
        dans un fichier text
        :return:
        """
        score = self.allTrucksDist + (self.allTrucksTime / 600) + (len(self.trajets) - 1) * 500
        result = False

        if self.best_score == 0:
            self.best_score = score
            for s in self.solutions:
                self.best_route.append(s['indicesClients'])
        if self.best_score > score:
            self.best_result = self.trajets
            self.best_score = score
            self.best_route = []
            for s in self.solutions:
                self.best_route.append(s['indicesClients'])
            result = True

        flat_list = self.get_last_solution_as_list(self.best_route)
        self.list_solution = flat_list
        self.export_solution_depending_on_algo_case(self.func_index)
        return result

    def add_travel_attributes(self):
        """
        A chaque fois qu'un vehicule est en decide de prendre une livraison en plus
        On rajoute les differente valeurs a ses contraintes pour pouvoir analyser
        s'il peut prendre plus
        :return:
        """
        self.sol.append(self.adding_another_client)
        self.totalDist += float(self.mDistances[self.lastDemande][self.adding_another_client])
        self.totalCapacity += float(self.demandes[self.lastDemande])
        self.totalTime += self.mTimes[self.lastDemande][self.adding_another_client] + self.delivery_time()
        self.allTrucksTime += self.mTimes[self.lastDemande][self.adding_another_client] + self.delivery_time()

    def return_to_depot(self):
        """
        Idem que precedemment mais cette fois pour le retour au depot
        :return:
        """
        self.totalDist += float(self.mDistances[self.lastDemande][len(self.demandes)])
        self.totalTime += self.mTimes[self.lastDemande][len(self.demandes)]
        self.allTrucksTime += self.mTimes[self.lastDemande][len(self.demandes)]
        self.allTrucksDist += self.totalDist

    # We chose to create an heuristic that puts chooses the client in the normal order, however when the next order
    # is too much to take, we check the remaining order to find one that can be added instead.
    # If we can we put it else we send it in the next trip
    def execute_heuristic(self, heuristic_choice):
        for self.func_index in range(1, 5):
            for self.client_index in range(-1, len(self.demandes)):
                client_list_by_index = self.initialize_heuristic_by_voisinage_order(self.client_index, heuristic_choice)
                # initialise variables for a new run of the algorithm. As such we need to initialise the different list
                # of elements of the heuristic such as the client list in the solution
                # but also a list of their coordinates.
                # We use a dictionary for the solution with one attribute
                # being the vehicle number and the other the trip
                # it will have to make that day
                self.j = client_list_by_index[0]
                k = 1
                self.newVehicle = True
                self.lastDemande = -1
                self.indicesClients = []
                self.trajets = []
                self.solutions = []
                self.sol = []
                current_solution_list = []
                # We also initialise the variables needed to compute the score
                self.allTrucksDist = 0
                self.allTrucksTime = 0
                self.numV = 0
                self.nbRetoursBase = 0
                self.adding_another_client = False

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
                        if self.lastDemande in current_solution_list:
                            self.lastDemande = self.j
                            self.j = client_list_by_index[k]
                            k += 1

                        else:
                            coordonees.append(self.coords[self.j])
                            self.indicesClients.append(self.lastDemande)
                            current_solution_list.append(self.lastDemande)

                            self.totalDist += float(self.mDistances[self.lastDemande][self.j])
                            self.totalCapacity += float(self.demandes[self.lastDemande])
                            self.totalTime += self.mTimes[self.lastDemande][self.j] + self.delivery_time()
                            self.allTrucksTime += self.mTimes[self.lastDemande][self.j] + self.delivery_time()
                            self.newVehicle = False
                            self.lastDemande = self.j
                            self.j = client_list_by_index[k]
                            k += 1

                    else:
                        self.adding_another_client = self.check_if_demande_fits()
                        if self.adding_another_client != 0 and self.respects_time_distance_constraints() \
                                and (self.adding_another_client not in current_solution_list):
                            self.indicesClients.append(self.adding_another_client)
                            current_solution_list.append(self.adding_another_client)
                            coordonees.append(self.coords[self.adding_another_client])

                            self.add_travel_attributes()
                        else:
                            self.return_to_depot()

                        if self.after_vehicule_recharge_still_time_left():
                            coordonees.append(self.coords[len(self.demandes)])
                            # Vehicle returned to base and is preparing to be sent out again
                            # As such we recharge it (adding the charging time) and
                            # reset its total distance and capacity
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
                            trajet["indicesClients"] = self.indicesClients
                            self.solutions.append(solution)
                            self.indicesClients = [-1]
                            self.newVehicle = True

                    if k - 1 > len(self.demandes):
                        self.allTrucksDist += self.totalDist
                        trajet["coordonees"] = coordonees
                        self.trajets.append(trajet)
                        self.indicesClients.append(-1)

                        solution["indicesClients"] = self.indicesClients
                        trajet["indicesClients"] = self.indicesClients
                        self.solutions.append(solution)
                        self.indicesClients = [-1]
                        break

                # On verifie si le score de cette solution est
                # meilleur que la meilleure solution trouvee
                # On remplace l'acienne par celle-ci si elle est meilleure
                score = self.best_score_solution()
                if score:
                    if heuristic_choice == 3 or heuristic_choice == 4:
                        self.func_index += 1
                        self.client_index = len(self.demandes)
                        break
        return self.best_result