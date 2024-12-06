import os
import pandas as pd
from incident_importer import IncidentImporter
from mobilization_importer import MobilisationImporter
from data_merge import DataMerger
from colorama import Fore, Style, init
from datetime import datetime
from DataVisualizer import DataVisualizer

# Initialisation de colorama
init()

def print_with_time(message):
    """
    Affiche un message avec l'heure actuelle en orange.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(Fore.YELLOW + f"{current_time} - {message}" + Style.RESET_ALL)

print(Fore.CYAN + f'################################################################' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------ #' + Style.RESET_ALL)
print(Fore.CYAN + f'# Exploitation des fichiers incidents via la classe spécifique #' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------ #' + Style.RESET_ALL)
print(Fore.CYAN + f'################################################################' + Style.RESET_ALL)
start_time = datetime.now()  # Enregistrer l'heure de début

# Chemin complet du fichier avec 30% des données
incidents_sample_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/incidents_sample_2020_30_percent.xlsx"

# Vérification de l'existence du fichier de 30%
if os.path.isfile(incidents_sample_filepath):
    print_with_time("Le fichier avec 30% des données existe déjà. Aucune exécution nécessaire.")
else:
    print_with_time("Fichier avec 30% des données non trouvé. Exécution de l'échantillonnage.")
    incident_path = "C:/Users/lukas/Desktop/Git Repo/csv_files/LFB Incident data from 2018 onwards.csv"

    # Instanciation de la classe avec un seul chemin de fichier
    print_with_time("Importation des données d'incidents...")
    incidentData = IncidentImporter(incident_file_path=incident_path)

    # Appel de la méthode pour charger les données
    df_incidents = incidentData.get_data()

    if df_incidents is not None:
        print_with_time("Création d'un échantillon de 30% des incidents...")
        sample_df = df_incidents.sample(frac=0.3, random_state=1)
        # sample_df = sample_df.columns.str.replace('ï»¿', '', regex=False)
        sample_df.to_excel("incidents_sample_2020_30_percent.xlsx", index=False)
        print_with_time("Échantillon de 30% enregistré dans 'incidents_sample_2020_30_percent.xlsx'")
    else:
        print(Fore.RED + "Erreur : Aucun fichier n'a été chargé avec succès." + Style.RESET_ALL)


end_time = datetime.now()  # Enregistrer l'heure de fin
duration = end_time - start_time
print(Fore.LIGHTMAGENTA_EX + f"Durée d'exécution de la méthode 'IncidentImporter' : {duration}" + Style.RESET_ALL)

print(Fore.CYAN + f'###################################################################' + Style.RESET_ALL)
print(Fore.CYAN + f'# --------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'# Exploitation des fichiers mobilization via la classe spécifique #' + Style.RESET_ALL)
print(Fore.CYAN + f'# --------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'###################################################################' + Style.RESET_ALL)
start_time = datetime.now()  # Enregistrer l'heure de début

# Chemin complet du fichier avec les données concaténées de mobilisation
mobilization_sample_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/mobilization_sample_2020.xlsx"
linked_mobilization_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/linked_mobilization.xlsx"

# Vérification de l'existence du fichier de mobilisation concaténé
if os.path.isfile(mobilization_sample_filepath):
    print_with_time("Le fichier avec les données de mobilisation concaténées existe déjà. Aucune exécution nécessaire.")
else:
    print_with_time("Fichier avec les données de mobilisation concaténées non trouvé. Exécution de la concaténation des données.")
    
    # Liste des chemins des fichiers mobilisations
    mobilization_paths = [
        "C:/Users/lukas/Desktop/Git Repo/csv_files/LFB Mobilisation data from 2015 - 2020.xlsx",
        "C:/Users/lukas/Desktop/Git Repo/csv_files/LFB Mobilisation data 2021 - 2024.xlsx"
    ]
    
    # Importation des données de mobilisation
    print_with_time("Importation des données de mobilisation...")
    mobiliData = MobilisationImporter(mobilization_paths)
    df_concat = mobiliData.get_dataframe()

    df_concat.to_excel(mobilization_sample_filepath, index=False)
    print_with_time("Données de mobilisation concaténées enregistrées dans 'mobilization_sample_2020.xlsx'")

end_time = datetime.now()  # Enregistrer l'heure de fin
duration = end_time - start_time
print(Fore.LIGHTMAGENTA_EX + f"Durée d'exécution de la méthode 'MobilizationImporter' : {duration}" + Style.RESET_ALL)


print_with_time(f"Vérification du fichier : {linked_mobilization_filepath}")

if os.path.isfile(linked_mobilization_filepath):
    print_with_time("Le fichier de mobilisation linked existe déjà")
else:
    print_with_time("Fichier avec les données de mobilisation linked non trouvé. Exécution de la concaténation des données.")
    start_time = datetime.now()  # Enregistrer l'heure de début

    if os.path.isfile(mobilization_sample_filepath):
        print_with_time("Le fichier de mobilisation fusionnée existe déjà. Chargement des données...")
        try:
            df_concat = pd.read_excel(mobilization_sample_filepath, engine='openpyxl')
            print_with_time(f"Fichier mobilization chargé avec {len(df_concat)} lignes.")
        except Exception as e:
            print_with_time(Fore.RED + f"Erreur lors du chargement du fichier de mobilisation : {e}" + Style.RESET_ALL)
            df_concat = pd.DataFrame()

        # Charger le fichier incidents
        try:
            df_incidents_30 = pd.read_excel(incidents_sample_filepath, engine='openpyxl')
            df_incidents_30.columns = df_incidents_30.columns.str.replace('ï»¿', '', regex=False)
            print_with_time(f"Fichier incidents chargé avec {len(df_incidents_30)} lignes.")
        except Exception as e:
            print_with_time(Fore.RED + f"Erreur lors du chargement du fichier des incidents : {e}" + Style.RESET_ALL)
            df_incidents_30 = pd.DataFrame()

        # Vérification des colonnes
        if 'IncidentNumber' in df_incidents_30.columns and 'IncidentNumber' in df_concat.columns:
            print_with_time("Filtrage des mobilisations correspondant aux incidents...")
            filtered_df = df_concat[df_concat['IncidentNumber'].isin(df_incidents_30['IncidentNumber'])]
            print_with_time(f"Nombre de lignes après filtrage : {len(filtered_df)}")
        else:
            df_incidents_30.columns.to_list()
            df_concat.columns.to_list()
            print_with_time(Fore.RED + "Erreur : La colonne 'IncidentNumber' est absente." + Style.RESET_ALL)
            filtered_df = pd.DataFrame()

        # Enregistrement des données filtrées
        try:
            if filtered_df is not None and not filtered_df.empty:
                filtered_df.to_excel(linked_mobilization_filepath, index=False)
                print_with_time("Données de mobilisation concaténées enregistrées dans 'linked_mobilization.xlsx'")
            else:
                print_with_time(Fore.RED + "Erreur : le DataFrame filtré est vide, aucune donnée enregistrée." + Style.RESET_ALL)
        except Exception as e:
            print_with_time(Fore.RED + f"Erreur lors de l'enregistrement du fichier : {e}" + Style.RESET_ALL)
 
        end_time = datetime.now()  # Enregistrer l'heure de fin
        duration = end_time - start_time
        print(Fore.LIGHTMAGENTA_EX + f"Durée d'exécution de la méthode 'linked_files' : {duration}" + Style.RESET_ALL)
    else:
        print_with_time(Fore.RED + "Fichier de mobilisation fusionnée introuvable !" + Style.RESET_ALL)


# Fusion des données incidents et mobilisations
print(Fore.CYAN + f'#################################################################' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'#    Data merger permettant la création d un nouveau fichier    #' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'#################################################################' + Style.RESET_ALL) 
start_time = datetime.now()  # Enregistrer l'heure de début

merged_sample_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/merged_incidents_mobilizations_2020.xlsx"

if os.path.isfile(merged_sample_filepath):
    print_with_time("Le fichier avec les données mergées existe déjà. Aucune exécution nécessaire.")
else:
    print_with_time("Fusion des données incidents et mobilisations...")

    # Instance de DataMerger
    merger = DataMerger(incidents_sample_filepath, linked_mobilization_filepath)
    df_merged = merger.merge_data()

    if not df_merged.empty:
        output_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/merged_incidents_mobilizations.xlsx"
        try:
            print_with_time("Enregistrement des données fusionnées...")
            df_merged.to_excel(output_filepath, index=False, engine='openpyxl')
            print_with_time(f"Fusion réussie. Fichier enregistré à : {output_filepath}")
        except Exception as e:
            print(Fore.RED + f"Erreur lors de l'enregistrement du fichier fusionné : {e}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Aucune donnée fusionnée à enregistrer." + Style.RESET_ALL)


end_time = datetime.now()  # Enregistrer l'heure de fin
duration = end_time - start_time
print(Fore.LIGHTMAGENTA_EX + f"Durée d'exécution de la méthode 'mergedFiles' : {duration}" + Style.RESET_ALL)

print(Fore.CYAN + f'#################################################################' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'#                   Génération des graphiques                   #' + Style.RESET_ALL)
print(Fore.CYAN + f'# ------------------------------------------------------------- #' + Style.RESET_ALL)
print(Fore.CYAN + f'#################################################################' + Style.RESET_ALL)
start_time = datetime.now()  # Enregistrer l'heure de début

input_filepath = "C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/merged_incidents_mobilizations.xlsx"
visualizer = DataVisualizer(input_filepath)

# 1. Evolution du temps de réponse moyen par an
visualizer.plot_mean_attendance_per_year()
# 2. Evolution du nombre d'incidents traités par an et par type
visualizer.plot_incident_counts_per_group()
# 3. Top 5 des casernes avec le plus d'interventions par type d'incident
visualizer.plot_top_5_stations()
# 4. Top 5 des casernes avec le moins d'interventions par type d'incident
visualizer.plot_least_5_stations()
# 5. Temps de réponse en fonction de la nature de l'incident
visualizer.plot_response_time_by_incident_type()
# 6. Affichage des valeurs uniques dans 'StopCodeDescription' et leur nombre d'occurrences
visualizer.print_stop_code_description_counts()
# 7. Affichage de la heatmap des corrélations entre les variables
visualizer.plot_heatmap()

end_time = datetime.now()  # Enregistrer l'heure de fin
duration = end_time - start_time
print(Fore.LIGHTMAGENTA_EX + f"Durée d'exécution de la méthode 'mergedFiles' : {duration}" + Style.RESET_ALL)