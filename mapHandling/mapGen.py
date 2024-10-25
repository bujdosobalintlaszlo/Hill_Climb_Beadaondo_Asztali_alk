import numpy as np
from scipy.ndimage import gaussian_filter
import os

instance_count = 0
map_size = 0
min_height, max_height = 0, 150
map_counter = 1

def get_valid_int_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Kérlek, adj meg egy számot {min_value} és {max_value} között!")
            else:
                return value
        except ValueError:
            print("Érvényes egész számot adj meg!")

def initialize_inputs():
    global instance_count, map_size
    instance_count = get_valid_int_input('Hány map generálódjon?: ', 1, None)
    map_size = get_valid_int_input('Add meg a pályaméretet (min.: 10, max.: 100): ', 10, 100)

def generate_maps():
    global map_counter
    for i in range(instance_count):
        map_data = np.random.randint(min_height, max_height + 1, (map_size, map_size))
        sigma = 2
        smoothed_map = gaussian_filter(map_data, sigma=sigma)
        write_into_file(smoothed_map)
        map_counter += 1

def write_into_file(smoothed_map):
    global map_counter
    file_name = f'maps/map{map_counter}.txt'
    os.makedirs('maps', exist_ok=True)
    with open(file_name, 'w') as f:
        max_heights = CheckMultipleMaxes(smoothed_map)
        f.write(f'{", ".join(map(str, max_heights.astype(int)))}\n')
        for row in smoothed_map:
            f.write(' '.join(map(str, row.astype(int))) + '\n')
    print(f'Kész a(z) {map_counter}/{instance_count} map')

def CheckMultipleMaxes(smoothed_map):
    flattened_map = smoothed_map.flatten()
    max_val = flattened_map.max()
    return flattened_map[flattened_map == max_val]

initialize_inputs()
generate_maps()



