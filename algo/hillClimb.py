import os
import random

# Itt irom ki az eremneyt fileba, olvasom azt be a modositashoz, illetve olvasom be a mappot.
class FileHandling:

    # konstruktor
    def __init__(self, file_number):
        # A hasznalt file szama. Ez futtatasnal fontos mivel a fileok is igy vannak elnevezve. Pl.:(map1.txt vagy result1.txt)
        self.file_number = file_number
        # Az eredmeny utvonala
        self.result_file_path = f'../mapHandling/results/result{self.file_number}.txt'
        #A map utvonala
        self.map_file_path = f'../mapHandling/maps/map{self.file_number}.txt'

    #map beolvasasa
    def read_map(self):
        map_data = []
        with open(self.map_file_path, 'r') as file:
            maxArr = file.readline().strip().replace(',', '').split(' ')
            global_max = int(maxArr[0])
            
            for line in file:
                line_cleaned = line.strip().replace(',', '').split(' ')
                temp_arr = [int(num) for num in line_cleaned if num.isdigit()]
                map_data.append(temp_arr)
        
        #visszaadjuk a mappot es a globalis max(okat)
        return map_data, global_max

    # Itt probaljuk beolvasni az eddigi eredmenyeket. Ha letezik a file beolvassuk es visszadjuk, ha nem egy ures tombel terunk vissza
    def read_latest_data(self):
        if not os.path.exists(self.result_file_path):
            return []
        
        with open(self.result_file_path, 'r') as r:
            lines = r.readlines()
            if not lines:
                return []
            data = lines[0].strip().split(',')
            # a formatum [lepesszam atlag, futtatasok szama]
            return data

    # Itt mentjuk a fileba az adatokat. Ha ures tombot kaptunk read_latest_data()-bol akkor a lepesszamot es 1 et irunk a fileba, egyebkent
    # pedig atlagot szamolunk es a futtatas szamot novelunk. A formatum pl.: 591.00, 3
    def save_result(self, step_counter):
        latest_data = self.read_latest_data()
        #uj file mert meg nincs
        if len(latest_data) == 0:
            with open(self.result_file_path, 'w') as w:
                w.write(f'{step_counter}, 1')
            return
        #adatok kiszamolasa
        previous_simulation_count = int(latest_data[1])
        new_simulation_count = previous_simulation_count + 1
        average_steps = (step_counter + float(latest_data[0]) * previous_simulation_count) / (new_simulation_count)
        
        #adatok beirasa
        with open(self.result_file_path, 'w') as w:
            w.write(f'{average_steps:.2f}, {new_simulation_count}')

# Maga a hill climer algo
class HillClimber:
    #konstruktor
    def __init__(self, file_number):
        self.file_handler = FileHandling(file_number)
        self.map, self.global_max = self.file_handler.read_map()
        self.global_maxes = []
        self.stepCounter = 0

    # Random szomszed visszaadasa
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
        
        random.shuffle(neighbors)  # Shuffle to add randomness
        
        return neighbors

   # hillclimb algo
    def hill_climb(self, start_x, start_y, visited):
        current_x, current_y = start_x, start_y
        
        while True:
            current_value = self.map[current_x][current_y]
            next_move = self.get_best_neighbor(current_x, current_y, visited)
            
            if next_move is None:
                break

            current_x, current_y = next_move
            visited.add((current_x, current_y))

        self.update_global_max(current_x, current_y, current_value)

    # optimalis szomszed kivalasztasa a kovetkezo lepeshez
    def get_best_neighbor(self, current_x, current_y, visited):
        current_value = self.map[current_x][current_y]
        neighbors = self.get_neighbors(current_x, current_y)
        best_value = current_value
        next_move = None
        
        for nx, ny in neighbors:
            neighbor_value = self.map[nx][ny]
            
            if neighbor_value > best_value and (nx, ny) not in visited:
                best_value = neighbor_value
                next_move = (nx, ny)
                self.stepCounter += 1
                
        return next_move

    # globalmax ellenorzes
    def update_global_max(self, current_x, current_y, current_value):
        if current_value > self.global_max:
            self.global_max = current_value
            self.global_maxes = [(current_x, current_y)]
        elif current_value == self.global_max:
            if (current_x, current_y) not in self.global_maxes:
                self.global_maxes.append((current_x, current_y))

    # osszes globalis max megkeresese
    def find_all_global_maxes(self):
        rows = len(self.map)
        cols = len(self.map[0])
        visited = set()

        # Addig megyunk amig az osszes cella meg lesz latogatva
        while len(visited) < rows * cols:
            # Random nem meglatogatott cella
            (x, y) = (random.randint(0, rows - 1), random.randint(0, cols - 1))

            # Ha a cella nem volt meglatogatva akkor onnan kezdi a keresest
            if (x, y) not in visited:
                self.hill_climb(x, y, visited)
                visited.add((x, y))

        # Logolas globalis max(ok) helyei
        print(f"Global maximum value: {self.global_max} found at: {self.global_maxes} with count: {len(self.global_maxes)}")
        # Megtett lepesek szama
        print(f"Total steps taken: {self.stepCounter}")
    # Eredmenyek mentese
    def save_result(self):
        self.file_handler.save_result(self.stepCounter)

# Program futtatasa
if __name__ == "__main__":
    current_file_number = 3
    climber = HillClimber(current_file_number)
    climber.find_all_global_maxes()
    climber.save_result()











            