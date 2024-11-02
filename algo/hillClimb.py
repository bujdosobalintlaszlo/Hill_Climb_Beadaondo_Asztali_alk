import os

import random

class HillClimber:
    def __init__(self, file_number):
        self.map = []
        self.global_max = float('-inf')
        self.global_maxes = []
        self.read_map(file_number)
        self.stepCounter = 0
        self.file_number = file_number
    
        
    def read_map(self, file_number):
        file_path = f'../mapHandling/maps/map{file_number}.txt'
        
        with open(file_path, 'r') as file:
            maxArr = file.readline().strip().replace(',', '').split(' ')
            self.global_max = int(maxArr[0])
            
            for line in file:
                line_cleaned = line.strip().replace(',', '').split(' ')
                temp_arr = [int(num) for num in line_cleaned if num.isdigit()]
                self.map.append(temp_arr)

    def get_neighbors(self, x, y):
        neighbors = []
        rows = len(self.map)
        cols = len(self.map[0])
        
        if x > 0: 
            neighbors.append((x - 1, y))
        if x < rows - 1: 
            neighbors.append((x + 1, y))
        if y > 0: 
            neighbors.append((x, y - 1))
        if y < cols - 1: 
            neighbors.append((x, y + 1))
        
        # Randomize the order of neighbors
        random.shuffle(neighbors)
        
        return neighbors

    def hill_climb(self, start_x, start_y, visited):
        current_x, current_y = start_x, start_y
        
        while True:
            current_value = self.map[current_x][current_y]
            neighbors = self.get_neighbors(current_x, current_y)
            next_move = None
            best_value = current_value
            
            for nx, ny in neighbors:
                neighbor_value = self.map[nx][ny]
                
                if neighbor_value > best_value and (nx, ny) not in visited:
                    best_value = neighbor_value
                    next_move = (nx, ny)
                    self.stepCounter += 1  # Increment step count only on valid moves
            
            if next_move is None:
                break

            current_x, current_y = next_move
            visited.add((current_x, current_y))  # Add visited cell

        # Update global max
        if current_value > self.global_max:
            self.global_max = current_value
            self.global_maxes = [(current_x, current_y)]
        elif current_value == self.global_max:
            if (current_x, current_y) not in self.global_maxes:
                self.global_maxes.append((current_x, current_y))

    def find_all_global_maxes(self):
        rows = len(self.map)
        cols = len(self.map[0])
        visited = set()

        # Continue until all cells are visited
        while len(visited) < rows * cols:
            # Pick a random unvisited starting point
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)

            # If the cell hasn't been visited, start hill climbing from there
            if (x, y) not in visited:
                print(f"Starting hill climb from random point: ({x}, {y})")  # Debugging
                self.hill_climb(x, y, visited)
                visited.add((x, y))  # Mark as visited after hill climbing
        
        # After all cells have been checked
        print(f"Global maximum value: {self.global_max} found at: {self.global_maxes} with count: {len(self.global_maxes)}")
        print(f"Total steps taken: {self.stepCounter}")


    # igy menti a program a eredmenyt, ha nincs meg neki kulon file letrehoz egyet beleirja a stepCountot es h 1. futtatas ha van akkor beleirja az atlagot, plussz a futtatas szamat
    def save_result(self):
        latest_data = self.read_latest_data(self.file_number)
        if len(latest_data) == 0:
            with open(f'../mapHandling/results/result{self.file_number}.txt', 'w') as w:
                w.write(f'{self.stepCounter}, 1')
            return

        previous_total_steps = float(latest_data[0])
        previous_simulation_count = int(latest_data[1])
        new_simulation_count = previous_simulation_count + 1
        average_steps = (self.stepCounter + previous_total_steps * previous_simulation_count) / (new_simulation_count)
        
        with open(f'../mapHandling/results/result{self.file_number}.txt', 'w') as w:
            w.write(f'{average_steps:.2f}, {new_simulation_count}')

    def read_latest_data(self, current_file_number):
        file_path = f'../mapHandling/results/result{current_file_number}.txt'
        
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r') as r:
            lines = r.readlines()
            
            if not lines:
                return []

            data = lines[0].strip().split(',')
            
        return data


# Program execution
if __name__ == "__main__":
    current_file_number = 2
    climber = HillClimber(current_file_number)
    climber.find_all_global_maxes()
    climber.save_result()











            