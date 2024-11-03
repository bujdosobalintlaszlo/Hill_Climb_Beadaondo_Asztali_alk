import os
import random
from tqdm import tqdm

class HillClimber:
    def __init__(self, file_number):
        self.map = []
        self.global_max = float('-inf')
        self.global_maxes = []
        self.stepCounter = 0
        self.file_number = file_number
        self.tabu_list = set() 
        self.tabu_list_size = 30

        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.map_directory = os.path.join(current_directory, '../mapHandling/maps')
        self.results_directory = os.path.join(current_directory, '../mapHandling/results')

        self.read_map(file_number)

    def read_map(self, file_number):
        file_path = os.path.join(self.map_directory, f'map{file_number}.txt')
        
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
            
        return neighbors

    def hill_climb(self, start_x, start_y, visited):
        current_x, current_y = start_x, start_y
        rows = len(self.map)
        cols = len(self.map[0])
        
        while True:
            current_value = self.map[current_x][current_y]
            neighbors = self.get_neighbors(current_x, current_y)
            next_move = None
            best_value = current_value
            
            neighbors.sort(key=lambda pos: self.map[pos[0]][pos[1]], reverse=True)

            for nx, ny in neighbors:
                neighbor_value = self.map[nx][ny]

                if (nx, ny) in self.tabu_list and neighbor_value <= best_value:
                    continue

                if neighbor_value > best_value:
                    best_value = neighbor_value
                    next_move = (nx, ny)
                    self.stepCounter += 1

            if next_move is None:
                break
            
            current_x, current_y = next_move
            self.tabu_list.add((current_x, current_y))

            if len(self.tabu_list) > self.tabu_list_size:
                self.tabu_list.pop()

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

        for _ in range(rows * cols):
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)

            if (x, y) not in visited:
                self.hill_climb(x, y, visited)
                visited.add((x, y))

    def save_result(self):
        latest_data = self.read_latest_data(self.file_number)
        
        if len(latest_data) == 0:
            with open(os.path.join(self.results_directory, f'result{self.file_number}.txt'), 'w') as w:
                w.write(f'{self.stepCounter}, 1')
            return

        previous_total_steps = float(latest_data[0])
        previous_simulation_count = int(latest_data[1])
        new_simulation_count = previous_simulation_count + 1
        average_steps = (self.stepCounter + previous_total_steps * previous_simulation_count) / new_simulation_count
        
        with open(os.path.join(self.results_directory, f'result{self.file_number}.txt'), 'w') as w:
            w.write(f'{average_steps:.2f}, {new_simulation_count}')

        self.stepCounter = 0


    def read_latest_data(self, current_file_number):
        file_path = os.path.join(self.results_directory, f'result{current_file_number}.txt')
        
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r') as r:
            lines = r.readlines()
            
            if not lines:
                return []

            data = lines[0].strip().split(',')
            
        return data


if __name__ == "__main__":
    total_runs = int(input("Hányszor fusson le a szimuláció egy mappra: "))
    total_maps = int(input("Hány mappra fusson le: "))

    for j in range(total_maps):
        current_file_number = j + 1
        climber = HillClimber(current_file_number)

        with tqdm(total=total_runs, desc=f"Map {current_file_number}", unit="run") as pbar:
            for i in range(total_runs):
                climber.find_all_global_maxes()
                climber.save_result()
                pbar.update(1)

        climber.stepCounter = 0

    print('A program lefutott.')
    input('Ha vissza szeretnél lépni zárd nyomj egy ENTER-t...')
