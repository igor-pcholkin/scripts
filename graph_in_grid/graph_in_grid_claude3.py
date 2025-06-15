import networkx as nx
import matplotlib.pyplot as plt
import math
import random

def create_graph(connections_dict):
    G = nx.Graph()
    for node, neighbors in connections_dict.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    return G

def calculate_grid_size(num_nodes):
    return math.ceil(math.sqrt(num_nodes))

def optimize_layout(G, grid_size):
    # Use spring_layout with a large scale to spread out the nodes
    pos = nx.spring_layout(G, k=1/(math.sqrt(len(G.nodes()))*0.3), iterations=50)
    
    # Scale and shift the positions to fit in our grid
    min_x = min(coord[0] for coord in pos.values())
    max_x = max(coord[0] for coord in pos.values())
    min_y = min(coord[1] for coord in pos.values())
    max_y = max(coord[1] for coord in pos.values())
    
    grid_pos = {}
    used_positions = set()
    
    for node in G.nodes():
        x, y = pos[node]
        # Scale to fit grid_size and round to nearest integer
        x_scaled = round((x - min_x) / (max_x - min_x) * (grid_size - 1))
        y_scaled = round((y - min_y) / (max_y - min_y) * (grid_size - 1))
        
        # Ensure the position is unique
        while (x_scaled, y_scaled) in used_positions:
            # If position is taken, try to find a nearby free spot
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
                new_x, new_y = x_scaled + dx, y_scaled + dy
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and (new_x, new_y) not in used_positions:
                    x_scaled, y_scaled = new_x, new_y
                    break
            else:
                # If no nearby spot is free, choose a random free position
                free_positions = set((x, y) for x in range(grid_size) for y in range(grid_size)) - used_positions
                if not free_positions:
                    raise ValueError("Not enough space in the grid for all nodes")
                x_scaled, y_scaled = random.choice(list(free_positions))

        grid_pos[node] = (x_scaled, y_scaled)
        used_positions.add((x_scaled, y_scaled))
    
    return grid_pos

def print_grid(G, pos, grid_size):
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    for node, (x, y) in pos.items():
        grid[grid_size - 1 - y][x] = node
    
    for row in grid:
        print(' '.join(row))

def visualize_graph(G, pos, grid_size):
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=16, font_weight='bold')
    plt.title("Graph Visualization")
    plt.xlim(-1, grid_size)
    plt.ylim(-1, grid_size)
    plt.xticks(range(grid_size))
    plt.yticks(range(grid_size))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Example input
    connections_dict = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    G = create_graph(connections_dict)
    grid_size = calculate_grid_size(len(G.nodes))
    pos = optimize_layout(G, grid_size)
    
    print(f"Grid size: {grid_size}x{grid_size}")
    print_grid(G, pos, grid_size)
    
    visualize_graph(G, {node: (x, grid_size-1-y) for node, (x, y) in pos.items()}, grid_size)

if __name__ == "__main__":
    main()
