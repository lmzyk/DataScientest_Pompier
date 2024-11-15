import pandas as pd
from colorama import Fore, Style, init

class DataMerger:
    def __init__(self, incidents_filepath, mobilizations_filepath):
        """
        Initialise la classe avec les chemins vers les fichiers incidents et mobilisations.
        
        :param incidents_filepath: Chemin du fichier contenant les 30% des incidents
        :param mobilizations_filepath: Chemin du fichier contenant les mobilisations concaténées
        """
        self.incidents_filepath = incidents_filepath
        self.mobilizations_filepath = mobilizations_filepath

    def merge_data(self):
        # Chargement des fichiers incidents et mobilisations
        df_incidents = pd.read_excel(self.incidents_filepath, engine='openpyxl')
        df_mobilizations = pd.read_excel(self.mobilizations_filepath, engine='openpyxl')

        # Merge sur IncidentNumber, en conservant les colonnes incidents et ajoutant uniquement celles de mobilisation
        df_merged = pd.merge(
            df_incidents, 
            df_mobilizations, 
            on='IncidentNumber', 
            how='left'
        )

        # Sauvegarde du DataFrame résultant
        merged_filepath = "merged_incidents_mobilizations.xlsx"
        df_merged.to_excel(merged_filepath, index=False)
        print(f"Fichier de données fusionnées enregistré sous : {merged_filepath}")
        return df_merged