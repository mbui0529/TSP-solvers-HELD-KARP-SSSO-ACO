from utility import *
from held_karp import held_karp
from ssso import local_best_first, local_beam, local_restart
import csv

def experiment2():
    size = 10
    N = 100
    hk = []
    best_first = []
    beam = []
    best_first_restart = []
    beam_restart = []
    for i in range(N):
        dists = generate_distances(size)
        cost, path = held_karp(dists)
        hk.append(cost)
        cost, path = local_best_first(size,dists)
        best_first.append(cost)
        cost, path = local_beam(size,dists)
        beam.append(cost)
        cost, path = local_restart(size, dists,local_best_first)
        best_first_restart.append(cost)
        cost, path = local_restart(size, dists,local_beam)
        beam_restart.append(cost)
        print("Finish loop no: ", i)

    result = [hk, best_first, beam, best_first_restart, beam_restart]
    with open('experiment2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)

print("Start the experiment no 2\n")
experiment2()