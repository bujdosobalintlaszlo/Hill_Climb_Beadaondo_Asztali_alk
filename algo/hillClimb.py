import random

class HillClimber:

    # konstruktor
    def __init__(self, file_number):
        self.map = []
        self.global_max = float('-inf')
        self.global_maxes = []
        self.read_map(file_number)

    # filebeolvasas
    def read_map(self, file_number):
        file_path = f'../mapHandling/maps/map{file_number}.txt'
        
        with open(file_path, 'r') as file:
            maxArr = file.readline().strip().replace(',', '').split(' ')
            self.global_max = int(maxArr[0])
            
            for line in file:
                line_cleaned = line.strip().replace(',', '').split(' ')
                temp_arr = [int(num) for num in line_cleaned if num.isdigit()]
                self.map.append(temp_arr)

    # szomszedos ertekek checkolasa
    def get_neighbors(self, x, y):
        neighbors = []
        rows = len(self.map)
        cols = len(self.map[0])
        
        if x > 0: 
            neighbors.append((x - 1, y))  # Up
        if x < rows - 1: 
            neighbors.append((x + 1, y))  # Down
        if y > 0: 
            neighbors.append((x, y - 1))  # Left
        if y < cols - 1: 
            neighbors.append((x, y + 1))  # Right
            
        return neighbors

    # hill climb algo
    def hill_climb(self, start_x, start_y, visited):
        current_x, current_y = start_x, start_y
        rows = len(self.map)
        cols = len(self.map[0])
        
        while True:
            current_value = self.map[current_x][current_y]
            neighbors = self.get_neighbors(current_x, current_y)
            next_move = None
            best_value = current_value
            
            # osszes szomszed check es a legnagyobb kivalasztasa ezek kozul
            for nx, ny in neighbors:
                neighbor_value = self.map[nx][ny]
                if neighbor_value > best_value:
                    best_value = neighbor_value
                    next_move = (nx, ny)

            # Ha egyik szomszed sem nagyobb akk local maxon vagyunk
            if next_move is None:
                break
            
            # Lepes a "legjobb"(legnagyobb) szomszedra 
            current_x, current_y = next_move
            print(f"Moving to {(current_x, current_y)} with value {best_value}")

        # megnezi h az uj lokalmax az a global max-e
        if current_value > self.global_max:
            self.global_max = current_value
            self.global_maxes = [(current_x, current_y)]
        elif current_value == self.global_max:
            if (current_x, current_y) not in self.global_maxes:
                self.global_maxes.append((current_x, current_y))

        print(f"Reached local maximum at {(current_x, current_y)} with value {self.map[current_x][current_y]}")

    # maxok szama es azok helye
    def find_all_global_maxes(self):
        rows = len(self.map)
        cols = len(self.map[0])
        visited = set()

        for x in range(rows):
            for y in range(cols):
                if (x, y) not in visited:
                    print(f"Starting hill climb from {(x, y)}")
                    self.hill_climb(x, y, visited)
                    visited.add((x, y))
        print(f"Global maximum value: {self.global_max} found at: {self.global_maxes} with count: {len(self.global_maxes)}")


# Program futtatasa
if __name__ == "__main__":
    current_file_number = 4
    climber = HillClimber(current_file_number)
    climber.find_all_global_maxes()




            