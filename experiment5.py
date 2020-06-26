from utility import *
from held_karp import held_karp
from aco import ACO,Graph
from ssso import local_best_first, local_restart, local_beam
import csv
import time

def experiment5():
    size = [50, 100, 500]
    for s in size:
        dists = generate_distances(s)
        aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
        graph = Graph(dists, s)
        start_time = time.time()
        path, cost = aco.solve(graph,timeout=60)
        t = time.time()-start_time
        print("ACO Solution. cost: {}, path: {}".format(cost, path))
        print("ACO Solution. size: {}, time: {}".format(s, t))
        print('')
        """
        start_time = time.time()
        cost, path = local_restart(s, dists,local_best_first,timeout=60)
        t = time.time() - start_time

        print("SSSO. cost: {}, path: {}".format(cost, path))
        print("SSSO. size: {}, time: {}".format(s, t))
        print('')
        """
        start_time = time.time()
        cost, path = local_restart(s, dists, local_beam, timeout=60)
        t = time.time() - start_time


        print("SSSO. cost: {}, path: {}".format(cost, path))
        print("SSSO. size: {}, time: {}".format(s, t))

print("Start the experiment no 5\n")
experiment5()