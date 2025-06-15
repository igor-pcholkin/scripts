import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def find_nearest_free_position(grid, x, y, grid_size):
    """Find the nearest free position in the grid around the (x, y) coordinates."""
    for dx in range(-grid_size, grid_size + 1):
        for dy in range(-grid_size, grid_size + 1):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if (new_x, new_y) not in grid.values():
                    return new_x, new_y
    raise ValueError("No free position found")  # In case the grid is full.

def place_objects_in_grid(relationships, grid_size):
    # Create graph from relationships dictionary
    G = nx.Graph(relationships)

    # Create an initial layout using a force-directed algorithm
    pos = nx.spring_layout(G)  # Use spring layout to get an initial position

    # Scale the positions to fit within a grid of the given size
    scale_factor = grid_size - 1
    grid_positions = {}
    
    print (pos)
    for node, (x, y) in pos.items():
        # Scale positions to fit into the grid
        grid_x = int(np.clip(x * scale_factor, 0, scale_factor))
        grid_y = int(np.clip(y * scale_factor, 0, scale_factor))
        
        # If the position is already occupied, find a new free position
        if (grid_x, grid_y) in grid_positions.values():
            grid_x, grid_y = find_nearest_free_position(grid_positions, grid_x, grid_y, grid_size)
        
        grid_positions[node] = (grid_x, grid_y)

    return (grid_positions, G)

# Example relationships dictionary
relationships = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'E'],
    'D': ['B', 'F'],
    'E': ['C', 'F'],
    'F': ['D', 'E']
}

# Define the size of the grid (e.g., 3x3)
grid_size = 3  # Make sure the grid is large enough to fit all objects

# Place objects on the grid
(grid_positions, G) = place_objects_in_grid(relationships, grid_size)

# Print the grid positions
print("Grid positions:", grid_positions)

# Optionally, visualize the graph with grid positions
plt.figure(figsize=(5, 5))
nx.draw(G, pos=grid_positions, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
plt.grid(True)
plt.show()
