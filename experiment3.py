from utility import *
from held_karp import held_karp
from aco import ACO,Graph
from ssso import local_beam, local_best_first, local_restart
import csv

def experiment3():
    size = 15
    N = 10
    hk = []
    ant = []
    beam_restart = []
    for i in range(N):
        dists = generate_distances(size)
        cost, path = held_karp(dists)
        hk.append(cost)
        aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
        graph = Graph(dists, size)
        path, cost = aco.solve(graph)
        ant.append(cost)
        cost, path = local_restart(size, dists,local_best_first)
        beam_restart.append(cost)
        print("Finish loop no: ", i)

    result = [hk, ant, beam_restart]
    with open('experiment3.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)

print("Start the experiment no 3\n")
experiment3()