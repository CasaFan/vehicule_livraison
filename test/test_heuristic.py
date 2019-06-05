from unittest import TestCase
import random
from src.modele.Heuristic import *
from src.modele.VehicleConfiguration import VehicleConfiguration
import numpy as np

data = {
    'distances': [],
    'times': [],
    'coordinates': [],
    'demands': []
}
v = VehicleConfiguration(250, 100, 60, 180, 12, "123", "456")
heuristic = Heuristic(data, v)


class TestHeuristic(TestCase):

    def test_get_index_list(self):
        # Normal case
        my_list1 = [10, 1, 24, 32, 12]
        index1 = heuristic.get_index_list(my_list1, 1)
        self.assertEqual(index1, [0, 1, 2, 3, 4, 5, -1])

    def test_get_index_list_for_solution(self):
        # Normal case
        my_list1 = [10, 1, 24, 32, 12]
        index1 = heuristic.get_index_list_for_solution(my_list1)
        self.assertEqual(index1, [10, 1, 24, 32, 12, 5, -1])

    def test_premier_voisinage(self):
        # Normal case
        my_list = [0, 1, 2, 3, 4, 4, -1]
        my_range = 1
        my_sol = [0, 2, 1, 3, 4, 4, -1]
        self.assertEqual(my_sol, heuristic.premier_voisinage(my_range, my_list))

        # Out of range
        my_list2 = [0, 1, 2, 3, 4, 4, -1]
        my_range2 = 4
        my_sol2 = [4, 1, 2, 3, 0, 4, -1]
        self.assertEqual(my_sol2, heuristic.premier_voisinage(my_range2, my_list2))

    def test_deuxieme_voisinage(self):
        # Normal case
        my_list = [0, 1, 2, 3, 4, 4, -1]
        my_range = 1
        my_sol = [0, 3, 2, 1, 4, 4, -1]
        self.assertEqual(my_sol, heuristic.deuxieme_voisinage(my_range, my_list))

        # Out of range
        my_list2 = [0, 1, 2, 3, 4, 4, -1]
        my_range2 = 4
        my_sol2 = [0, 1, 2, 3, 4, 4, -1]
        self.assertEqual(my_sol2, heuristic.deuxieme_voisinage(my_range2, my_list2))

        # Empty list
        my_list3 = []
        my_range3 = 1
        my_sol3 = []
        self.assertEqual(my_sol3, heuristic.deuxieme_voisinage(my_range3, my_list3))

    def test_troisieme_voisinage(self):
        # Normal case
        my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1]
        my_range = 1
        my_sol = [0, 8, 7, 6, 5, 4, 3, 2, 1, 9, 10, -1]
        self.assertEqual(my_sol, heuristic.troisieme_voisinage(my_range, my_list))

        # Out of range
        my_list2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1]
        my_range2 = 2
        my_sol2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1]
        self.assertEqual(my_sol2, heuristic.troisieme_voisinage(my_range2, my_list2))

        # Empty list
        my_list3 = []
        my_range3 = 1
        my_sol3 = []
        self.assertEqual(my_sol3, heuristic.troisieme_voisinage(my_range3, my_list3))

    def test_check_if_demande_fits(self):
        # Normal case
        heuristic.demandes = [10, 20, 30]
        heuristic.totalCapacity = 20
        heuristic.capacity = 40
        heuristic.lastDemande = 1
        my_return = heuristic.check_if_demande_fits()
        my_sol = 1
        self.assertEqual(my_sol, my_return)

        # Case False
        heuristic.demandes = [10, 20, 30]
        heuristic.totalCapacity = 40
        heuristic.capacity = 20
        heuristic.lastDemande = 2
        self.assertFalse(heuristic.check_if_demande_fits())

    def test_respects_time_capacity_distance_constraints(self):
        heuristic.lastDemande = 0
        heuristic.j = 1

        heuristic.demandes = [10, 20, 30]
        heuristic.totalCapacity = 20
        heuristic.capacity = 40

        heuristic.mDistances = np.array([[0, 10, 20, 30], [10, 0, 20, 30], [10, 20, 0, 30], [10, 20, 30, 0]])
        heuristic.totalDist = 10
        heuristic.max_dist = 40

        heuristic.mTimes = np.array([[0, 500, 1000, 1500], [500, 0, 1000, 1500], [500, 1000, 0, 1500], [500, 1000, 1500, 0]])
        heuristic.totalTime = 400
        heuristic.deliveryTime = 100
        heuristic.endTime = 2000

        # Normal case
        self.assertTrue(heuristic.respects_time_capacity_distance_constraints())

        # Case False Distance
        heuristic.totalDist = 38
        self.assertFalse(heuristic.respects_time_capacity_distance_constraints())

        # Case False Time
        heuristic.totalDist = 10
        heuristic.totalTime = 1500
        self.assertFalse(heuristic.respects_time_capacity_distance_constraints())

        # Case False Capacity
        heuristic.totalTime = 400
        heuristic.totalCapacity = 38
        self.assertFalse(heuristic.respects_time_capacity_distance_constraints())

    def test_respects_time_distance_constraints(self):
        heuristic.adding_another_client = 0
        heuristic.j = 1

        heuristic.demandes = [10, 20, 30]

        heuristic.mDistances = np.array([[0, 10, 20, 30], [10, 0, 20, 30], [10, 20, 0, 30], [10, 20, 30, 0]])
        heuristic.totalDist = 10
        heuristic.max_dist = 40

        heuristic.mTimes = np.array(
            [[0, 500, 1000, 1500], [500, 0, 1000, 1500], [500, 1000, 0, 1500], [500, 1000, 1500, 0]])
        heuristic.totalTime = 400
        heuristic.deliveryTime = 100
        heuristic.endTime = 2000

        # Normal case
        self.assertTrue(heuristic.respects_time_distance_constraints())

        # Case False Distance
        heuristic.totalDist = 38
        self.assertFalse(heuristic.respects_time_distance_constraints())

        # Case False Time
        heuristic.totalDist = 10
        heuristic.totalTime = 1500
        self.assertFalse(heuristic.respects_time_distance_constraints())

    def test_after_vehicule_recharge_still_time_left(self):
        heuristic.adding_another_client = 0
        heuristic.j = 1

        heuristic.demandes = [10, 20, 30]

        heuristic.mTimes = np.array(
            [[0, 500, 1000, 1500], [500, 0, 1000, 1500], [500, 1000, 0, 1500], [500, 1000, 1500, 0]])
        heuristic.totalTime = 400
        heuristic.deliveryTime = 100
        heuristic.endTime = 15000

        # Normal case
        self.assertTrue(heuristic.after_vehicule_recharge_still_time_left())

        # Case False Time
        heuristic.totalTime = 10000
        self.assertFalse(heuristic.after_vehicule_recharge_still_time_left())

    def test_get_last_solution_as_list(self):
        my_list = [[0, 1, 2, -1, 3], [4, -1, 5, 3]]
        my_sol = [0, 1, 2, 3, 4, 5, 3]
        my_return = heuristic.get_last_solution_as_list(my_list)

        # Normal case
        self.assertEqual(my_sol, my_return)

        my_list = []
        my_sol = []
        my_return = heuristic.get_last_solution_as_list(my_list)

        # Empty list case
        self.assertEqual(my_sol, my_return)


