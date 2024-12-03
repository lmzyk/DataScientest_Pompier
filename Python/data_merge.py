import pandas as pd
from colorama import Fore, Style, init

class DataMerger:
    def __init__(self, incidents_filepath, mobilizations_filepath, merged_filepath="merged_incidents_mobilizations.xlsx"):
        """
        Initialise la classe avec les chemins vers les fichiers incidents et mobilisations,
        et un chemin de sortie pour le fichier fusionné.

        :param incidents_filepath: Chemin du fichier contenant les incidents filtrés.
        :param mobilizations_filepath: Chemin du fichier contenant les mobilisations concaténées.
        :param merged_filepath: Chemin du fichier où enregistrer les données fusionnées (par défaut 'merged_incidents_mobilizations.xlsx').
        """
        self.incidents_filepath = incidents_filepath
        self.mobilizations_filepath = mobilizations_filepath
        self.merged_filepath = merged_filepath

    def preprocess_data(self, df_incidents, df_mobilizations):
        """
        Prépare les données en ajustant les types et en mettant à jour les colonnes nécessaires.

        :param df_incidents: DataFrame des incidents.
        :param df_mobilizations: DataFrame des mobilisations.
        :return: DataFrames prétraités.
        """
        # Vérification des colonnes nécessaires
        required_columns_incidents = ['IncidentNumber', 'TimeOfCall']
        required_columns_mobilizations = ['IncidentNumber', 'DateAndTimeMobile']
        
        if not all(col in df_incidents.columns for col in required_columns_incidents):
            raise ValueError(f"Colonnes manquantes dans les incidents : {set(required_columns_incidents) - set(df_incidents.columns)}")
        if not all(col in df_mobilizations.columns for col in required_columns_mobilizations):
            raise ValueError(f"Colonnes manquantes dans les mobilisations : {set(required_columns_mobilizations) - set(df_mobilizations.columns)}")
        
        # Conversion des colonnes 'IncidentNumber' en string dans les deux DataFrames
        df_incidents['IncidentNumber'] = df_incidents['IncidentNumber'].astype(str)
        df_mobilizations['IncidentNumber'] = df_mobilizations['IncidentNumber'].astype(str)
        
        # Conversion des dates
        df_mobilizations['DateAndTimeMobile'] = pd.to_datetime(df_mobilizations['DateAndTimeMobile'], errors='coerce')
        df_incidents['TimeOfCall'] = pd.to_datetime(df_incidents['TimeOfCall'], format='%H:%M:%S', errors='coerce').dt.time
        
        # Mise à jour de la colonne 'DateOfCall' dans les incidents
        df_incidents['DateOfCall'] = df_mobilizations['DateAndTimeMobile'].dt.date

        print(Fore.GREEN + "Prétraitement des données effectué avec succès." + Style.RESET_ALL)
        return df_incidents, df_mobilizations

    def filter_data_from_2020(self, df_incidents, df_mobilizations):
        """
        Filtre les données pour ne garder que les lignes à partir de l'année 2020.

        :param df_incidents: DataFrame des incidents.
        :param df_mobilizations: DataFrame des mobilisations.
        :return: DataFrames filtrés.
        """
        # Vérification de l'existence de la colonne 'CalYear'
        if 'CalYear' not in df_incidents.columns or 'CalYear' not in df_mobilizations.columns:
            raise ValueError("Les colonnes 'CalYear' sont manquantes dans l'un des DataFrames.")
        
        df_incidents_filtered = df_incidents[df_incidents['CalYear'] >= 2020]
        df_mobilizations_filtered = df_mobilizations[df_mobilizations['CalYear'] >= 2020]

        print(Fore.YELLOW + "Données filtrées à partir de l'année 2020." + Style.RESET_ALL)
        return df_incidents_filtered, df_mobilizations_filtered

    def merge_data(self):
        """
        Charge les fichiers incidents et mobilisations, effectue le prétraitement, filtre les données et fusionne.
        
        :return: DataFrame fusionné.
        """
        try:
            # Chargement des fichiers incidents et mobilisations
            df_incidents = pd.read_excel(self.incidents_filepath, engine='openpyxl')
            df_mobilizations = pd.read_excel(self.mobilizations_filepath, engine='openpyxl')

            # Vérification du chargement des DataFrames
            if df_incidents.empty:
                raise ValueError("Le fichier des incidents est vide ou n'a pas été chargé correctement.")
            if df_mobilizations.empty:
                raise ValueError("Le fichier des mobilisations est vide ou n'a pas été chargé correctement.")
            
            # Vérification des colonnes de base
            print(f"Colonnes des incidents : {df_incidents.columns.tolist()}")
            print(f"Colonnes des mobilisations : {df_mobilizations.columns.tolist()}")
            
            # Prétraitement des données
            df_incidents, df_mobilizations = self.preprocess_data(df_incidents, df_mobilizations)

            # Filtrer les données à partir de 2020
            df_incidents, df_mobilizations = self.filter_data_from_2020(df_incidents, df_mobilizations)

            # Résumé des DataFrames avant fusion
            print(Fore.CYAN + f"Incidents avant fusion : {len(df_incidents)} lignes" + Style.RESET_ALL)
            print(Fore.CYAN + f"Mobilisations avant fusion : {len(df_mobilizations)} lignes" + Style.RESET_ALL)

            # Fusion des données sur 'IncidentNumber'
            df_merged = pd.merge(df_incidents, df_mobilizations, on='IncidentNumber', how='left')

            # Vérification après fusion
            if df_merged.empty:
                raise ValueError("La fusion a échoué : aucun résultat obtenu.")

            # Sauvegarde du DataFrame fusionné
            df_merged.to_excel(self.merged_filepath, index=False)
            print(Fore.BLUE + f"Fichier de données fusionnées enregistré sous : {self.merged_filepath}" + Style.RESET_ALL)

            # Résumé après fusion
            print(Fore.CYAN + f"Fusion terminée : {len(df_merged)} lignes fusionnées." + Style.RESET_ALL)
            
            return df_merged
        
        except FileNotFoundError as e:
            print(Fore.RED + f"Erreur lors du chargement des fichiers : {e}" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"Erreur de validation des données : {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Erreur inconnue : {e}" + Style.RESET_ALL)
