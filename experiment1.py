import time
from utility import *
from held_karp import held_karp

def experiment1():
    size = [10, 15, 20, 30]
    for s in size:
        dists = generate_distances(s)
        print_2D_matrix(dists)
        start_time = time.time()
        cost, path = held_karp(dists)
        t = time.time() - start_time
        print("Held Karp Solution. cost: {}, path: {}".format(cost, path))
        print("Held Karp Solution. size: {}, time: {}".format(s, t))
        print('')


print("Start the experiment no 1\n")
experiment1()