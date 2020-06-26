"""
Name: Matthew Bui
"""
from utility import scorer
import random
import time
import copy

def random_solver(instance_size):
    """
    :param instance_size [int]
    :return: path [list]
    """
    city = [i for i in range(1,instance_size)]  # City numbered from 0 to size -1
    path = [0] # Path start at city 0
    for i in range(1,instance_size):
        path.append(city.pop(random.randint(0,(instance_size-1-i))))
    return path

def best_initial_maker(instance_size,matrix,n_times):
    """
    select the best random solution in n times
    :param instance_size: problem size -> int
    :param matrix: distance matrix -> 2d array
    :param n_times: n trail -> int
    :return:
    """
    max_score = 0
    result = []
    for i in range(0,n_times):
        random_result = random_solver(instance_size)
        random_score = scorer(random_result,matrix)
        if random_score > max_score:
            max_score = random_score
            result = random_result
    return result


def transform(state, n):
    """
    swap second element to nth the elements.
    considered an element of Action set
    :param action: int
    :return: new_state
    """
    new_state = copy.deepcopy(state)
    new_state[1],new_state[n] = new_state[n],new_state[1]
    return new_state

def jump(state,n):
    """
    swap subset with size n in path
    considered an element of Action set
    :param state: array
    :param n: size of subset
    :return: new state
    """
    if n > (len(state) - 1)/2:
        n = int((len(state)-1)/2)
    new_state = copy.deepcopy(state)
    new_state[1:n], new_state[n:n*2] = new_state[n:n*2], new_state[1:n]
    return new_state


def best_jump(state,dist):
    """
    Consider all possible jumps and pick the best one. (Greedy)
    :param state: list
    :param dist: 2d matrix
    :return: best jumping state
    """
    min = 100000
    best_neighbor = []
    for i in range (2, int(len(state)/2)):
        new_state = jump(state, i+1)
        score = scorer(new_state, dist)
        if score <= min:
            min = score
            best_neighbor = new_state
    return best_neighbor


def best_transform(state,dist):
    """
    Consider the best transforming state (Greedy)
    :param state: list
    :param dist: 2d array
    :return: best transforming state
    """
    min = 100000
    best_neighbor = []
    for i in range (2, len(state)):
        new_state = transform(state, i)
        score = scorer(new_state, dist)
        if score <= min:
            min = score
            best_neighbor = new_state
    return best_neighbor

def best_transform_beam(state,dist,beam):
    """
    Pick Top beam possible transforming state. Greedy
    :param state: list
    :param dist: 2d array
    :param beam: number of top transforming state
    :return: array
    """
    neighbor = []
    result = []
    for i in range (2, len(state)):
        new_state = transform(state, i)
        score = scorer(new_state, dist)
        neighbor.append(new_state)
        result.append(score)
    return sorted(zip(result,neighbor ))[:beam]

def best_jump_beam(state,dist,beam):
    """
    Pick Top beam possible jumping state. Greedy
    :param state: list
    :param dist: 2d array
    :param beam: number of top jumping state
    :return: array
    """
    result = []
    neighbor = []
    for i in range (2, int(len(state)/2)):
        new_state = jump(state, i+1)
        score = scorer(new_state, dist)
        neighbor.append(new_state)
        result.append(score)
    return sorted(zip(result,neighbor ))[:beam]


def best_beam(beam, dist):
    """
    Select the best direction to go from top directions
    :param beam: array of direction
    :param dist: 2d array
    :return: state
    """
    min = 100000
    best = []
    for b in beam:
        next_trans = best_transform(b[1], dist)
        next_jump = best_jump(b[1], dist)
        score_tran = scorer(next_trans, dist)
        score_jump = scorer(next_jump, dist)
        if score_tran < score_jump:
            state = next_trans
            score = score_tran
        else:
            state = next_jump
            score = score_jump
        if score < min:
            best = state
            min = score
    return min,best

def local_best_first(instance,dist, timeout = 5):
    """
    Find the best neighbor and move
    :param instance: instance size
    :param dist: matrix
    :param dist: timeout to terminate the program
    :return: the best local state
    """
    # Set up hyper parameter:
    terminate = False
    start = time.time()

    # Set up the initial value
    state = best_initial_maker(instance,dist,1000)
    min_score = scorer(state,dist)
    while not terminate:
        next_trans = best_transform(state, dist)
        next_jump = best_jump(state,dist)
        score_tran = scorer(next_trans, dist)
        score_jump = scorer(next_jump,dist)

        if score_tran < score_jump:
            next_state = next_trans
            score_next = score_tran
        else:
            next_state = next_jump
            score_next = score_jump

        if score_next > min_score:
            terminate = True
        else:
            state = next_state
            min_score = score_next
        if (time.time()-start) > timeout:
            terminate = True
    return min_score,state

def local_beam(instance,dist, timeout = 5):
    """
    Find the best 3 neighbor and move
    :param instance: instance size
    :param dist: matrix
    :param dist: timeout to terminate the program
    :return: the best local state
    """
    # Set up hyper parameter:
    terminate = False
    start = time.time()
    beam = int(instance/3)
    # Set up the initial value
    state = best_initial_maker(instance,dist,1000)
    min_score = scorer(state, dist)
    while not terminate:
        next_trans = best_transform_beam(state, dist,beam)
        next_jump = best_jump_beam(state,dist,beam)
        best_direction = sorted(next_jump + next_trans)[:beam]
        score_next,next_state = best_beam(best_direction,dist)

        if score_next > min_score:
            terminate = True
        else:
            state = next_state
            min_score = score_next
        if (time.time()-start) > timeout:
            terminate = True
    return min_score,state


def local_restart(instance, dist, method,n_restart=100, timeout = 10):
    """
    Re-solve multiple times and pick the best one
    :param instance: size of problem
    :param dist: 2d array
    :param method: function
    :param n_restart: n restart times
    :param timeout: the limit of time
    :return:
    """
    min_score = 9999999
    result = []
    start = time.time()
    for _ in range(n_restart):
        cost, path = method(instance, dist,timeout=timeout)
        if cost < min_score:
            min_score = cost
            result = path
        if time.time() - start > timeout:
            return min_score,result
    return min_score,result




