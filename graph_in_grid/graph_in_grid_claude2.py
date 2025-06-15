import networkx as nx
import matplotlib.pyplot as plt
import math

def create_graph(connections_dict):
    G = nx.Graph(connections_dict)
    return G

def calculate_grid_size(num_nodes):
    return math.ceil(math.sqrt(num_nodes))

def optimize_layout(G, grid_size):
    # Use the spring layout algorithm to get initial positions
    #print(f"center: {int(grid_size / 2)}")
    center = int(grid_size / 2)
    pos = nx.spring_layout(G, center = [center, center], iterations = 100, k = math.sqrt(2))
    
    # Scale and shift the positions to fit in our grid
    min_x = min(coord[0] for coord in pos.values())
    max_x = max(coord[0] for coord in pos.values())
    min_y = min(coord[1] for coord in pos.values())
    max_y = max(coord[1] for coord in pos.values())
    
    for node in pos:
        x, y = pos[node]
        print(f"Node {node} before scaling: {x},{y}")
        x_scaled = (x - min_x) / (max_x - min_x) * (grid_size - 1)
        y_scaled = (y - min_y) / (max_y - min_y) * (grid_size - 1)
        print(f"Node {node} after scaling: {x_scaled},{y_scaled}")
        print(f"Node {node} after rounded scaling: {round(x_scaled)},{round(y_scaled)}")
        pos[node] = (round(x_scaled), round(y_scaled))
        #pos[node] = (round(x), round(y))
    
    return pos

def print_grid(G, pos, grid_size):
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    for node, (x, y) in pos.items():
        grid[grid_size - 1 - int(y)][int(x)] = node
    
    for row in grid:
        print(' '.join(row))

def visualize_graph(G, pos):
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=16, font_weight='bold')
    plt.title("Graph Visualization")
    plt.axis('off')
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
    
    visualize_graph(G, pos)

if __name__ == "__main__":
    main()
