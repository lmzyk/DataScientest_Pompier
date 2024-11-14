import os
import importlib
import csv_incident_library
importlib.reload(csv_incident_library)
from csv_incident_library import CSVHandler
from csv_mobilisation_library import MobilisationData
from csv_mobilisation_data_multiple_files import MobilisationDataMultipleFiles


# csv_path = os.path.join("csv_files", "fichier_fusionne.csv")
# csv_handler = CSVHandler(csv_path)
# csv_handler.init_csv()

# df_incident = csv_handler.get_dataframe()
# df_random_sample = df_incident.sample(frac=0.1, random_state=1)
# print(df_random_sample.head(5))



# Liste des chemins de fichiers à concaténer
file_paths = [
    "C:/Users/Lukas/Desktop/Formation/Projet/Python/csv_files/LFB Mobilisation data from January 2009 - 2014.xlsx",
    "C:/Users/Lukas/Desktop/Formation/Projet/Python/csv_files/LFB Mobilisation data from 2015 - 2020.xlsx",
    "C:/Users/Lukas/Desktop/Formation/Projet/Python/csv_files/LFB Mobilisation data 2021 - 2024.xlsx"
]

# Initialiser la classe avec la liste des fichiers
mobilisation_data = MobilisationDataMultipleFiles(file_paths)

# Obtenir le DataFrame fusionné
df_mobilisation = mobilisation_data.get_dataframe()

# Sélectionner un échantillon aléatoire de 30% et enregistrer dans un fichier Excel
if df_mobilisation is not None:
    sample_df = df_mobilisation.sample(frac=0.3, random_state=1)
    sample_df.to_excel("mobilisation_sample_30_percent.xlsx", index=False)
    print("Échantillon de 30% enregistré dans 'mobilisation_sample_30_percent.xlsx'")
else:
    print("Erreur : Aucun fichier n'a été chargé avec succès.")