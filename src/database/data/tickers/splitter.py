import pandas as pd
import os



def split_csv(file_path, lines_per_file):
    # Leer el archivo CSV
    df = pd.read_csv(file_path)

    # Calcular el número de archivos necesarios
    number_of_files = len(df) // lines_per_file + 1

    # Dividir el DataFrame y guardar cada parte como un nuevo archivo CSV
    for i in range(number_of_files):
        start_idx = i * lines_per_file
        end_idx = start_idx + lines_per_file
        df_part = df.iloc[start_idx:end_idx]
        df_part.to_csv(f'{file_path}.part{i}.csv', index=False)

# Uso
file_path = 'tickers.csv'

print(os.path.abspath(file_path))
lines_per_file = 100000  # Número de líneas por archivo
split_csv(file_path, lines_per_file)
