import math
import time

from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_random_neighbor

def simulated_annealing(current_cube, initial_temp, cooling_rate, max_iter):
    current_score = count_of_match(current_cube)
    temperature = initial_temp
    scores = [current_score]
    start = time.time()

    for i in range(max_iter):
        neighbor = generate_random_neighbor(current_cube)
        neighbor_score = count_of_match(neighbor)

        delta_score = neighbor_score - current_score

        if delta_score > 0:
            current_cube = neighbor
            current_score = neighbor_score
            scores.append(current_score)
        else:
            if delta_score > 0 or math.exp(delta_score / temperature) > 0.5:
                current_cube = neighbor
                current_score = neighbor_score
                scores.append(current_score)

        temperature *= cooling_rate

    end = time.time()
    duration = end - start

    return current_cube, current_score, scores, duration
