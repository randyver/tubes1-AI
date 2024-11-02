import time
from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_random_neighbor

def random_restart_hill_climbing(current_cube, iterations, max_restarts):
    count_restart = 0
    best_cube = current_cube
    best_score = count_of_match(current_cube)
    best_scores = [best_score]
    start_time = time.time()

    for i in range(max_restarts):
        count_restart += 1
        current_cube = best_cube
        current_score = best_score
        scores = [current_score]

        for j in range(iterations):
            neighbor = generate_random_neighbor(current_cube)
            new_score = count_of_match(neighbor)

            if new_score > current_score:
                current_cube, current_score = neighbor, new_score
                scores.append(current_score)

        if current_score > best_score:
            best_cube, best_score = current_cube, current_score
            best_scores = scores

    end_time = time.time()
    duration = end_time - start_time

    return count_restart, best_cube, best_score, best_scores, duration