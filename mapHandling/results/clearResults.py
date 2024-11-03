import os

base_dir = os.path.dirname(os.path.abspath(__file__))

inp = int(input('Hány resultot töröljön: '))
for i in range(inp):
    file_path = os.path.join(base_dir, f'result{i+1}.txt')
    with open(file_path, 'w') as w:
        w.write('')
print('A fájlok sikeresen ürítve!')
