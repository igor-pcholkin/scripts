import random
import math

class Object:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.connections = []

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
    connections_dict = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    objects = create_objects(connections_dict)
    grid_size = calculate_grid_size(len(objects))
    
    initial_placement(objects, grid_size)
    optimize_placement(objects, grid_size)
    
    print(f"Grid size: {grid_size}x{grid_size}")
    print_grid(objects, grid_size)

if __name__ == "__main__":
    main()
