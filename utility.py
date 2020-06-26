import random

def scorer(path,cost_matrix):
    """
    This function calculate the final score of the results.
    :param table (list)
    :return: (int)
    """
    cost = 0
    leng = len(path)
    for i in range (leng):
        if i < leng - 1:
            cost += cost_matrix[path[i]][path[i+1]]
        else:
            cost += cost_matrix[path[i]][0]
    return cost


# https://github.com/CarlEkerot/held-karp
def generate_distances(n):
    """
    generate distances based on size of the problem.
    :param n:
    :return: 2D mattrix
    """
    # Consider that the graph is symmetric
    d = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d[i][j] = d[j][i] = random.randint(1, 99)
    return d

# https://github.com/CarlEkerot/held-karp
def print_2D_matrix(matrix):
    for row in matrix:
        print(''.join([str(n).rjust(3, ' ') for n in row]))