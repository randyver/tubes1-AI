import numpy as np
import plotly.graph_objects as go

# Function to load and validate cube data from a file
def load_cube_data(filename):
    with open(filename, 'r') as file:
        data = file.read().split()
        numbers = [int(num) for num in data]
        
        # Check if we have exactly 125 numbers and they are all unique
        if len(numbers) != 125:
            raise ValueError("The file must contain exactly 125 numbers.")
        if len(set(numbers)) != 125:
            raise ValueError("All numbers in the file must be unique.")
        
        # Reshape into a 5x5x5 numpy array
        return np.array(numbers).reshape((5, 5, 5))

# Load cube data from file
cube_data = load_cube_data('test/benchmarkInput.txt')

# Function to check if a specific line or diagonal sums up to 315
def is_magic_sum(arr):
    return np.sum(arr) == 315

# Lists to store coordinates of magic elements
magic_coords = []

# Check rows, columns, planes, and room diagonals
for i in range(5):
    # Check rows
    for j in range(5):
        if is_magic_sum(cube_data[i, j, :]):
            magic_coords.extend([(i, j, k) for k in range(5)])
        if is_magic_sum(cube_data[i, :, j]):
            magic_coords.extend([(i, k, j) for k in range(5)])
        if is_magic_sum(cube_data[:, i, j]):
            magic_coords.extend([(k, i, j) for k in range(5)])

    # Check main plane diagonals
    if is_magic_sum(cube_data[i, range(5), range(5)]):
        magic_coords.extend([(i, k, k) for k in range(5)])
    if is_magic_sum(cube_data[i, range(5), range(4, -1, -1)]):
        magic_coords.extend([(i, k, 4 - k) for k in range(5)])
    if is_magic_sum(cube_data[range(5), i, range(5)]):
        magic_coords.extend([(k, i, k) for k in range(5)])
    if is_magic_sum(cube_data[range(5), i, range(4, -1, -1)]):
        magic_coords.extend([(k, i, 4 - k) for k in range(5)])
    if is_magic_sum(cube_data[range(5), range(5), i]):
        magic_coords.extend([(k, k, i) for k in range(5)])
    if is_magic_sum(cube_data[range(5), range(4, -1, -1), i]):
        magic_coords.extend([(k, 4 - k, i) for k in range(5)])

# Check room diagonals
if is_magic_sum(cube_data[range(5), range(5), range(5)]):
    magic_coords.extend([(k, k, k) for k in range(5)])
if is_magic_sum(cube_data[range(5), range(5), range(4, -1, -1)]):
    magic_coords.extend([(k, k, 4 - k) for k in range(5)])
if is_magic_sum(cube_data[range(5), range(4, -1, -1), range(5)]):
    magic_coords.extend([(k, 4 - k, k) for k in range(5)])
if is_magic_sum(cube_data[range(5), range(4, -1, -1), range(4, -1, -1)]):
    magic_coords.extend([(k, 4 - k, 4 - k) for k in range(5)])

# Remove duplicates from magic_coords
magic_coords = list(set(magic_coords))

# Prepare Plotly cubes (voxels)
fig = go.Figure()

# "Explosion" factor to spread layers apart
explosion_factor = 3

# Loop through each element in the cube_data and add it as a block in the 3D space
for i in range(5):
    for j in range(5):
        for k in range(5):
            # Apply the explosion factor for each axis
            x_pos = i * explosion_factor
            y_pos = j * explosion_factor
            z_pos = k * explosion_factor
            
            # Determine color based on whether the block is part of a "magic sum" line
            color = 'gold' if (i, j, k) in magic_coords else 'skyblue'
            
            # Create a small cube at each position (i, j, k)
            fig.add_trace(go.Mesh3d(
                x=[x_pos, x_pos+1, x_pos+1, x_pos, x_pos, x_pos+1, x_pos+1, x_pos],
                y=[y_pos, y_pos, y_pos+1, y_pos+1, y_pos, y_pos, y_pos+1, y_pos+1],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1, z_pos+1, z_pos+1, z_pos+1],
                color=color,
                opacity=0.5,
                alphahull=0,
                flatshading=True,
                hoverinfo='text',
                text=f"Value: {cube_data[i, j, k]}",
            ))
            # Add a label with the number inside each block
            fig.add_trace(go.Scatter3d(
                x=[x_pos + 0.5],
                y=[y_pos + 0.5],
                z=[z_pos + 0.5],
                mode='text',
                text=[str(cube_data[i, j, k])],
                textposition="middle center",
                textfont=dict(size=12, color="black")
            ))

# Update layout for 3D plot
fig.update_layout(
    title="5x5x5 Exploded Magic Cube Visualization",
    scene=dict(
        xaxis=dict(title="X", range=[-0.5, 5 * explosion_factor]),
        yaxis=dict(title="Y", range=[-0.5, 5 * explosion_factor]),
        zaxis=dict(title="Z", range=[-0.5, 5 * explosion_factor])
    ),
    scene_aspectmode='cube'  # Ensures all axes are scaled equally
)

fig.show()