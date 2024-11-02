import copy
import random

def generate_random_neighbor(cube):
    neighbor = copy.deepcopy(cube)
    i, j = random.sample(range(len(cube)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def generate_all_neighbors(current_cube):
    neighbors = []
    
    for i in range(125):
        for j in range(125):
            if i == j:
                continue
            
            neighbor = current_cube.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    
    return neighbors