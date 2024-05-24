import pandas as pd
import re
import os

def shift_row(row):
    if re.match(r'^€\s\d+\s\d+,-$', row['Column_3']) or re.match(r'^€\s\d+,-$', row['Column_3']):
        for i in range(len(row) - 1, 1, -1):
            row[i] = row[i - 1]
        row[1] = ''
    return row
    
output_folder = 'cars.xlsx'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
file_name = 'cars.csv'
file_full_path = os.path.join(file_name)
data = []
with open(file_full_path, 'r', encoding='utf-8') as file:
    for line in file:
        row = line.strip().split(';')
        data.append(row)
max_length = max(len(row) for row in data)

columns = [f'Column_{i+1}' for i in range(max_length)]

df = pd.DataFrame(data, columns=columns)

df.drop('Column_1', axis=1, inplace=True)
df.dropna(subset=['Column_3'], inplace=True)
df = df.apply(shift_row, axis=1)
df = df[:-2]

df.rename(columns={'Column_2': 'Autó', 'Column_3': 'Rövid leírás', 'Column_4': 'Ár',
                    'Column_5': 'Óra állás', 'Column_6': 'Váltó', 'Column_7': 'Évjárat',
                    'Column_8': 'Üzemanyag', 'Column_9': 'Teljesítmény', 'Column_10': 'Értékesítő',
                    'Column_11': 'Hely'}, inplace=True)

output_file_path = os.path.join("cars.xlsx")

df.to_excel(output_file_path, index=False)