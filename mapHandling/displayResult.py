import os

def display_result():
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Aktuális könyvtár
    results_directory = os.path.join(current_directory, 'results')  # Eredmények könyvtára

    while True:
        map_number = input('Add meg annak a mapnak a sorszámát, melynek eredményét szeretnéd látni (i - súgó): ')
        if map_number == "i":
            print('(1) A formátum pl.: 1\n(2) Figyelj arra, hogy ez a szám maximum akkora amennyi mappot generáltál generáltál.\n(3) A szám min. 1, mivel 1-től indexelődnek a fileok.\n')
        else:
            file_path = os.path.join(results_directory, f'result{map_number}.txt')  # Az eredmények elérési útja
            if os.path.isfile(file_path):
                data = read_data(file_path)
                print(f'Átlagos lépésszám: {data[0]}, futtatások száma: {data[1]}')
                break
            else:
                print('Hibás adat lett megadva. Ha elakadtál, írj egy "i" betűt.')

def read_data(file_path):
    with open(file_path, 'r') as r:
        return r.readline().strip().split(',')

display_result()
print('Nyomj meg egy billentyűt hogy visszalépj!')