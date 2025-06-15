import random
import math
import networkx as nx
import matplotlib.pyplot as plt

class Object:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.connections = []

def create_graph(objects):
		G = nx.Graph()
		for obj in objects:
				#print(f"Adding node {obj.id}, {obj.x}, {obj.y}, {obj}")
				G.add_node(obj.id, pos=(obj.x, obj.y))
				for connection in obj.connections:
						G.add_edge(obj.id, connection.id)
		return G
    
def visualize_graph(G, grid_size):
    pos = nx.get_node_attributes(G, 'pos')
    #print(f"pos: {pos}")
    #print(f"G: {G}")
    
    
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=False, node_color='lightblue', 
            node_size=500, font_size=7)
            
    nx.draw_networkx_labels(G, pos, font_size=7, font_color='black', 
                        font_family='sans-serif', font_weight='normal',
                        verticalalignment='top', horizontalalignment='center', clip_on = False)        
    
    # Draw edge labels
    #edge_labels = nx.get_edge_attributes(G, 'weight')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Object Graph Visualization")
    plt.xlim(-1, grid_size)
    plt.ylim(-1, grid_size)
    plt.xticks(range(grid_size))
    plt.yticks(range(grid_size))
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.tight_layout()
    plt.show()    

def create_objects(connections_dict):
    objects = {}
    for obj_id, connected_ids in connections_dict.items():
        if obj_id not in objects:
            objects[obj_id] = Object(obj_id)
        for connected_id in connected_ids:
            if connected_id not in objects:
                objects[connected_id] = Object(connected_id)
            objects[obj_id].connections.append(objects[connected_id])
            objects[connected_id].connections.append(objects[obj_id])
    return list(objects.values())

def calculate_grid_size(num_objects):
    grid_size = math.ceil(math.sqrt(num_objects))
    return grid_size

def initial_placement(objects, grid_size):
    positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    random.shuffle(positions)
    for obj, pos in zip(objects, positions):
        obj.x, obj.y = pos

def calculate_total_distance(objects):
    total_distance = 0
    for obj in objects:
        for connected_obj in obj.connections:
            dx = obj.x - connected_obj.x
            dy = obj.y - connected_obj.y
            total_distance += math.sqrt(dx**2 + dy**2)
    return total_distance

def optimize_placement(objects, grid_size, iterations=1000):
    best_distance = calculate_total_distance(objects)
    
    for _ in range(iterations):
        obj1, obj2 = random.sample(objects, 2)
        obj1.x, obj1.y, obj2.x, obj2.y = obj2.x, obj2.y, obj1.x, obj1.y
        
        new_distance = calculate_total_distance(objects)
        if new_distance < best_distance:
            best_distance = new_distance
        else:
            obj1.x, obj1.y, obj2.x, obj2.y = obj2.x, obj2.y, obj1.x, obj1.y

def print_grid(objects, grid_size):
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    for obj in objects:
        grid[obj.y][obj.x] = obj.id
    
    for row in grid:
        print(' '.join(row))

def main():
    # Example input
		theBeatlesLikes =[ "The Everly Brothers", "Chuck Berry", "Buddy Holly", "Little Richard", "Elvis Presley"]
		pinkFloysLikes = [ "The Rolling Stones", "The Beatles", "Cream", "The Velvet Underground", "Syd Barrett" ]
		smithsLikes = [ "The Velvet Underground", "The New York Dolls", "Roxy Music", "T. Rex", "David Bowie" ]
		talkingHeadsLikes = [ "The Velvet Underground", "Roxy Music", "David Bowie", "Brian Eno", "Parliament-Funkadelic" ]
		milesDavisLikes = [ "Duke Ellington", "Charlie Parker", "Dizzy Gillespie", "John Coltrane", "Thelonious Monk" ]
		aphexTwinsLikes = [ "Brian Eno", "Kraftwerk", "Karlheinz Stockhausen", "Tangerine Dream", "Cabaret Voltaire" ]
		kraftwerkLikes = [ "The Beach Boys", "The Velvet Underground", "The Beatles", "Karlheinz Stockhausen", "Neu!" ]
		canLikes = [ "The Velvet Underground", "Frank Zappa", "The Mothers of Invention", "Karlheinz Stockhausen", "The Beatles" ]
		remLikes = [ "The Byrds", "The Velvet Underground", "Patti Smith", "Big Star", "Television" ]
		davidBowieLikes = [ "The Velvet Underground", "The Beatles", "Little Richard", "Elvis Presley", "The Kinks" ]

		totalLikes = { "The Beatles": theBeatlesLikes, "Pink Floyd": pinkFloysLikes, "The Smiths": smithsLikes,
		"Talking Heads": talkingHeadsLikes, "Miles Davis": milesDavisLikes, "Aphex Twin": aphexTwinsLikes,
		"Kraftwerk": kraftwerkLikes, "Can": canLikes, "R.E.M.": remLikes, "David Bowie": davidBowieLikes }
    
		objects = create_objects(totalLikes)
		grid_size = calculate_grid_size(len(objects))
		
		initial_placement(objects, grid_size)
		optimize_placement(objects, grid_size)
		
		print(f"Grid size: {grid_size}x{grid_size}")
		print_grid(objects, grid_size)
		
		G = create_graph(objects)
		visualize_graph(G, grid_size)
		

if __name__ == "__main__":
    main()
