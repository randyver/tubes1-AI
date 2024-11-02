from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_all_neighbors

def steepest_ascent(current_cube):
    current_score = count_of_match(current_cube)
    
    while True:
        neighbors = generate_all_neighbors(current_cube)
        best_neighbor = None
        best_score = current_score
        
        for neighbor in neighbors:
            score = count_of_match(neighbor)
            if score > best_score:
                best_neighbor = neighbor
                best_score = score
        
        if best_neighbor is not None and best_score > current_score:
            current_cube = best_neighbor
            current_score = best_score
        else:
            break
    
    return current_cube, current_score