import math
import time

from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_random_neighbor

def simulated_annealing(current_cube, initial_temp, cooling_rate, max_iter):
    current_score = count_of_match(current_cube)
    temperature = initial_temp
    scores = [current_score]
    probabilities = []
    count_stuck = 0
    start = time.time()

    for i in range(max_iter):
        neighbor = generate_random_neighbor(current_cube)
        neighbor_score = count_of_match(neighbor)

        delta_score = neighbor_score - current_score

        if delta_score > 0:
            current_cube = neighbor
            current_score = neighbor_score
            scores.append(current_score)
            probabilities.append(1)
        else:
            probability = math.exp(delta_score / temperature)
            probabilities.append(probability)
            count_stuck += 1

            if probability > 0.5:
                current_cube = neighbor
                current_score = neighbor_score
                scores.append(current_score)

        temperature *= cooling_rate

    end = time.time()
    duration = end - start

    return max_iter, current_cube, current_score, scores, probabilities, count_stuck, duration
