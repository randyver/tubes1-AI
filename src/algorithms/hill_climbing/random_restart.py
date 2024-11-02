from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_random_neighbor

def random_restart_hill_climbing(current_cube, max_restarts=500, iterations=1000):
    best_cube = current_cube
    best_score = count_of_match(current_cube)

    for i in range(max_restarts):
        print(f"Restart number: {i + 1}")
        current_cube = generate_random_neighbor(current_cube)
        current_score = count_of_match(current_cube)

        for j in range(iterations):
            neighbor = generate_random_neighbor(current_cube)
            new_score = count_of_match(neighbor)

            if new_score > current_score:
                current_cube, current_score = neighbor, new_score

        if current_score > best_score:
            best_cube, best_score = current_cube, current_score

    return best_cube, best_score