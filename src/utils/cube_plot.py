import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

def load_cube_data(data_source):
    # Load data as before
    if isinstance(data_source, str):
        with open(data_source, 'r') as file:
            data = file.read().split()
            numbers = [int(num) for num in data]
    elif isinstance(data_source, (list, np.ndarray)):
        numbers = list(data_source)
    else:
        raise ValueError("Invalid data source. Must be a filename or an array of numbers.")
    
    if len(numbers) != 125 or len(set(numbers)) != 125:
        raise ValueError("Data must contain exactly 125 unique numbers.")
    
    return np.array(numbers).reshape((5, 5, 5))

def is_magic_sum(arr):
    return np.sum(arr) == 315

def find_magic_coordinates(cube_data):
    """
    Find cells in rows, columns, or diagonals that sum to 315, with match counts.
    Returns a dictionary where keys are coordinates and values are the count of matches.
    """
    magic_coords = defaultdict(int)

    for i in range(5):
        # Check rows, columns, and plane diagonals, counting matches
        for j in range(5):
            if is_magic_sum(cube_data[i, j, :]):
                for k in range(5):
                    magic_coords[(i, j, k)] += 1
            if is_magic_sum(cube_data[i, :, j]):
                for k in range(5):
                    magic_coords[(i, k, j)] += 1
            if is_magic_sum(cube_data[:, i, j]):
                for k in range(5):
                    magic_coords[(k, i, j)] += 1

        # Check main plane diagonals
        if is_magic_sum(cube_data[i, range(5), range(5)]):
            for k in range(5):
                magic_coords[(i, k, k)] += 1
        if is_magic_sum(cube_data[i, range(5), range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(i, k, 4 - k)] += 1
        if is_magic_sum(cube_data[range(5), i, range(5)]):
            for k in range(5):
                magic_coords[(k, i, k)] += 1
        if is_magic_sum(cube_data[range(5), i, range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(k, i, 4 - k)] += 1
        if is_magic_sum(cube_data[range(5), range(5), i]):
            for k in range(5):
                magic_coords[(k, k, i)] += 1
        if is_magic_sum(cube_data[range(5), range(4, -1, -1), i]):
            for k in range(5):
                magic_coords[(k, 4 - k, i)] += 1

    # Check room diagonals
    if is_magic_sum(cube_data[range(5), range(5), range(5)]):
        for k in range(5):
            magic_coords[(k, k, k)] += 1
    if is_magic_sum(cube_data[range(5), range(5), range(4, -1, -1)]):
        for k in range(5):
            magic_coords[(k, k, 4 - k)] += 1
    if is_magic_sum(cube_data[range(5), range(4, -1, -1), range(5)]):
        for k in range(5):
            magic_coords[(k, 4 - k, k)] += 1
    if is_magic_sum(cube_data[range(5), range(4, -1, -1), range(4, -1, -1)]):
        for k in range(5):
            magic_coords[(k, 4 - k, 4 - k)] += 1

    return magic_coords

def visualize_magic_cube(cube_data, magic_coords):
    fig = go.Figure()
    explosion_factor = 3
    color_map = {1: 'skyblue', 2: 'lightgreen', 3: 'gold', 4: 'orange', 5: 'red'}
    
    for i in range(5):
        for j in range(5):
            for k in range(5):
                x_pos, y_pos, z_pos = i * explosion_factor, j * explosion_factor, k * explosion_factor
                match_count = magic_coords.get((i, j, k), 0)
                color = color_map.get(match_count, 'gray')
                
                fig.add_trace(go.Mesh3d(
                    x=[x_pos, x_pos+1, x_pos+1, x_pos, x_pos, x_pos+1, x_pos+1, x_pos],
                    y=[y_pos, y_pos, y_pos+1, y_pos+1, y_pos, y_pos, y_pos+1, y_pos+1],
                    z=[z_pos, z_pos, z_pos, z_pos, z_pos+1, z_pos+1, z_pos+1, z_pos+1],
                    color=color,
                    opacity=0.6,
                    alphahull=0,
                    flatshading=True,
                    hoverinfo='text',
                    text=f"Value: {cube_data[i, j, k]} | Matches: {match_count}",
                ))
                fig.add_trace(go.Scatter3d(
                    x=[x_pos + 0.5],
                    y=[y_pos + 0.5],
                    z=[z_pos + 0.5],
                    mode='text',
                    text=[str(cube_data[i, j, k])],
                    textposition="middle center",
                    textfont=dict(size=12, color="black")
                ))

    fig.update_layout(
        title="5x5x5 Exploded Magic Cube Visualization",
        scene=dict(
            xaxis=dict(title="X", range=[-0.5, 5 * explosion_factor]),
            yaxis=dict(title="Y", range=[-0.5, 5 * explosion_factor]),
            zaxis=dict(title="Z", range=[-0.5, 5 * explosion_factor])
        ),
        scene_aspectmode='cube'
    )

    fig.show()

def main(data_source):
    cube_data = load_cube_data(data_source)
    magic_coords = find_magic_coordinates(cube_data)
    visualize_magic_cube(cube_data, magic_coords)
