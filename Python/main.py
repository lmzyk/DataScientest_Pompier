import os
import pandas as pd
from incident_importer import IncidentImporter
from csv_mobilisation_library import MobilisationData
from csv_mobilisation_data_multiple_files import MobilisationDataMultipleFiles
from data_merge import DataMerger
from colorama import Fore, Style, init


################################################################
# ------------------------------------------------------------ #
# Exploitation des fichiers incidents via la classe spécifique #
# ------------------------------------------------------------ #
################################################################

# Chemin complet du fichier avec 30% des données
incidents_sample_filepath = "G:/Git Repo/DataScientest_Pompier/Python/incidents_sample_30_percent.xlsx"

# Vérification de l'existence du fichier de 30%
if os.path.isfile(incidents_sample_filepath):
    print(Fore.YELLOW + f"Le fichier avec 30% des données existe déjà. Aucune exécution nécessaire." + Style.RESET_ALL)
else:
    print(Fore.GREEN + f"Fichier avec 30% des données non trouvé. Exécution de l'échantillonnage." + Style.RESET_ALL)

    # Remplacer les chemins par ceux des fichiers
    incident_paths=['G:/Git Repo/DataScientest_Pompier/csv_files/London fire brigade incident/LFB Incident data from 2009 - 2017.csv'
                    , 'G:/Git Repo/DataScientest_Pompier/csv_files/London fire brigade incident/LFB Incident data from 2018 onwards.csv']

    incidentData = IncidentImporter(incident_file_paths=incident_paths)

    df_filtered = incidentData.get_data()

    if df_filtered is not None:
        sample_df = df_filtered.sample(frac=0.3, random_state=1)
        sample_df.to_excel("incidents_sample_30_percent.xlsx", index=False)
        print("Échantillon de 30% enregistré dans 'incidents_sample_30_percent.xlsx'")
    else:
        print(Fore.RED, "Erreur : Aucun fichier n'a été chargé avec succès." + Style.RESET_ALL)



###################################################################
# --------------------------------------------------------------- #
# Exploitation des fichiers mobilization via la classe spécifique #
# --------------------------------------------------------------- #
###################################################################


# Chemin complet du fichier avec les données concaténées de mobilisation
mobilization_sample_filepath = "G:/Git Repo/DataScientest_Pompier/Python/mobilization_sample.xlsx"

# Vérification de l'existence du fichier de mobilisation concaténé
if os.path.isfile(mobilization_sample_filepath):
    print(Fore.YELLOW + f"Le fichier avec les données de mobilisation concaténées existe déjà. Aucune exécution nécessaire." + Style.RESET_ALL)
else:
    print(Fore.GREEN + f"Fichier avec les données de mobilisation concaténées non trouvé. Exécution de la concaténation des données." + Style.RESET_ALL)

    # Liste des chemins des fichiers mobilisations
    mobilization_paths = [
        "G:/Git Repo/DataScientest_Pompier/csv_files/London fire brigade mobilisation/LFB Mobilisation data from January 2009 - 2014.xlsx",
        "G:/Git Repo/DataScientest_Pompier/csv_files/London fire brigade mobilisation/LFB Mobilisation data from 2015 - 2020.xlsx",
        "G:/Git Repo/DataScientest_Pompier/csv_files/London fire brigade mobilisation/LFB Mobilisation data 2021 - 2024.xlsx"
    ]
    
    
    # Importation des données de mobilisation
    mobiliData = MobilisationData(mobilization_paths)
    df_concat = mobiliData.get_dataframe()

    df_incidents_30 = pd.read_excel(incidents_sample_filepath, engine='openpyxl')   # Charger le fichier de 30 %

    # Extraire uniquement les lignes de mobilisations correspondant aux IncidentNumber du fichier d'incidents de 30 %
    filtered_df = df_concat[df_concat['IncidentNumber'].isin(df_incidents_30['IncidentNumber'])]

    # Enregistrement des données concaténées dans un fichier Excel
    if filtered_df is not None:
        filtered_df.to_excel(mobilization_sample_filepath, index=False)
        print(Fore.GREEN + "Données de mobilisation concaténées enregistrées dans 'mobilization_sample.xlsx'" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Erreur lors de la concaténation des données de mobilisation." + Style.RESET_ALL)



#################################################################
# ------------------------------------------------------------- #
#    Data merger permettant la création d'un nouveau fichier    #
# ------------------------------------------------------------- #
#################################################################

# Chemin complet du fichier avec 30% des données mergées
merged_sample_filepath = "G:/Git Repo/DataScientest_Pompier/Python/merged_incidents_mobilizations.xlsx"

# Vérification de l'existence du fichier de 30%
if os.path.isfile(merged_sample_filepath):
    print(Fore.YELLOW + f"Le fichier avec les données mergées existe déjà. Aucune exécution nécessaire." + Style.RESET_ALL)
else:
    print(Fore.GREEN + f"Fichier avec les données mergées non trouvé. Exécution de l'échantillonnage." + Style.RESET_ALL)

    # # Création d'une instance de DataMerger
    merger = DataMerger(incidents_sample_filepath, mobilization_sample_filepath)

# Effectuer la fusion et obtenir le DataFrame filtré
    df_merged = merger.merge_data()

    # Vérification si la fusion a réussi et export du résultat
    if not df_merged.empty:
        output_filepath = "G:/Git Repo/DataScientest_Pompier/Python/merged_incidents_mobilizations.xlsx"
        try:
            df_merged.to_excel(output_filepath, index=False, engine='openpyxl')
            print(Fore.GREEN + f"Fusion réussie. Fichier enregistré à : {output_filepath}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Erreur lors de l'enregistrement du fichier fusionné : {e}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Aucune donnée fusionnée à enregistrer." + Style.RESET_ALL)
