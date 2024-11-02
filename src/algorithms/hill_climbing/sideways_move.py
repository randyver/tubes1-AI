from utils.count_of_match import count_of_match
from utils.neighbor_generator import generate_all_neighbors

def sideways_move(current_cube, max_sideways_moves=10):
    current_score = count_of_match(current_cube)
    sideways_moves = 0
    
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
            sideways_moves = 0
        elif best_neighbor is not None and best_score == current_score and sideways_moves < max_sideways_moves:
            current_cube = best_neighbor
            current_score = best_score
            sideways_moves += 1
        else:
            break
    
    return current_cube, current_score