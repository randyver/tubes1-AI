import time
from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_random_neighbor

def stochastic_hill_climbing(current_cube, iterations):
    current_score = count_of_match(current_cube)
    scores = [current_score]
    start_time = time.time()

    for i in range(iterations):
        neighbor = generate_random_neighbor(current_cube)
        new_score = count_of_match(neighbor)

        if new_score > current_score:
            current_cube, current_score = neighbor, new_score
            scores.append(current_score)

    end_time = time.time()
    duration = end_time - start_time

    return current_cube, current_score, scores, duration