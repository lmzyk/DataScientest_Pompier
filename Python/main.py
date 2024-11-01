import os
import importlib
import csv_library
importlib.reload(csv_library)
from csv_library import CSVHandler

csv_path = os.path.join("csv_files", "fichier_fusionne.csv")
csv_handler = CSVHandler(csv_path)
csv_handler.init_csv()

df_incident = csv_handler.get_dataframe()
df_random_sample = df_incident.sample(frac=0.1, random_state=1)
print(df_random_sample.head(5))