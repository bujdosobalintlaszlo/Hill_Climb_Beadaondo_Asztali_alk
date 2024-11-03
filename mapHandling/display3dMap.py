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
    """Check if the specified map file exists and read it."""
    global map_name
    maps_dir = os.path.join(os.path.dirname(__file__), 'maps')
    map_file_path = os.path.join(maps_dir, f'{map_name}.txt')

    if os.path.isfile(map_file_path):
        read_map(map_file_path)
    else:
        print("A megadott map fájl nem létezik.")

def read_map(file_path):
    """Read map data from a file and handle errors."""
    global map_data, max_peek
    try:
        with open(file_path, 'r') as f:
            first_line = next(f).strip()
            max_peek = int(''.join(filter(str.isdigit, first_line.split()[0])))
            map_data = [list(map(int, line.split())) for line in f]

            if not map_data:
                raise ValueError("A megadott fájl üres.")

            print("Map adat sikeresen beolvasva.")
            input('Ha vissza szeretnél lépni zárd nyomj egy ENTER-t...')
    except FileNotFoundError:
        print(f"A fájl nem található: {file_path}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Hiba történt a fájl beolvasásakor: {e}")

def display_image():
    """Display the terrain map as a 3D surface plot."""
    global map_data
    terrain_map = np.array(map_data)

    if terrain_map.ndim != 2:
        print("A terep térkép nem 2D.")
        return

    sigma = 2 
    smoothed_terrain_map = gaussian_filter(terrain_map, sigma=sigma)
    setup_3d_image(smoothed_terrain_map)

def setup_3d_image(terrain_map):
    """Set up and display the 3D surface plot."""
    x = np.arange(cols)
    y = np.arange(rows)
    x, y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, terrain_map, cmap='terrain', edgecolor='none')

    ax.set_title(f'{map_name}.txt')
    ax.set_zlabel('Magasság')

    plt.show()

check_if_valid_map()

if map_data:
    display_image()
