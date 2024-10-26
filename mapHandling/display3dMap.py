import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
import os

map_data = []
map_name = input("Add meg a map nevét (NEM KELL A *.txt): ")
rows, cols = 30, 30
min_height, max_height = 0, 150
max_peek = 0

def check_if_valid_map():
    global map_name
    while not os.path.isfile(f'maps/{map_name}.txt'):
        print("A megadott map fájl nem létezik.")
        map_name = input("Add meg a map nevét (NEM KELL A *.txt): ")
    read_map(f'maps/{map_name}.txt')

def read_map(map_name):
    global map_data, max_peek
    with open(map_name, 'r') as f:
        first_line = next(f).strip()
        max_peek = int(first_line.split()[0])
        map_data = [list(map(int, line.split())) for line in f]
    print("Map adat sikeresen beolvasva.")

def display_image():
    global map_data
    terrain_map = np.array(map_data)
    sigma = 2
    smoothed_terrain_map = gaussian_filter(terrain_map, sigma=sigma)
    setup_3d_image(smoothed_terrain_map)

def setup_3d_image(terrain_map):
    x = np.arange(cols)
    y = np.arange(rows)
    x, y = np.meshgrid(x, y)

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, terrain_map, cmap='terrain', edgecolor='none')

    ax.set_title(f'{map_name}.txt')
    ax.set_zlabel('Magasság')

    plt.show()

check_if_valid_map()
display_image()

