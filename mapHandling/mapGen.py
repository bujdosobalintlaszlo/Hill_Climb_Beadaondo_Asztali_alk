import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
import os

instance_count = 0
map_size = 0
min_height, max_height = 0, 150

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
    instance_count = get_valid_int_input('Hány map generálódjon?', 1, None)
    map_size = get_valid_int_input('Add meg a pályaméretet (min.: 10, max.: 100)', 10, 100)

initialize_inputs()

