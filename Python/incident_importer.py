import pandas as pd
from colorama import Fore, Style, init
from datetime import datetime

# Initialisation de colorama
init(autoreset=True)

class IncidentImporter:
    def __init__(self, incident_file_path):
        self.incident_file_path = incident_file_path
        self.columns_to_keep = [
            'IncidentNumber', 'DateOfCall', 'CalYear', 'TimeOfCall', 'HourOfCall',
            'IncidentStationGround', 'NumStationsWithPumpsAttending', 'PumpCount',
            'IncidentGroup', 'StopCodeDescription', 'ProperCase', 'Notional Cost (£)',
            'Latitude', 'Longitude', 'AddressQualifier'
        ]
        
        # Print : Début de l'importation
        self._print_action("Début de l'importation du fichier CSV.")

        # Chargement du fichier CSV
        self.df_incid_2018 = pd.read_csv(incident_file_path, encoding='unicode_escape', sep=';')
        self._print_action("Fichier CSV chargé avec succès.")

        # Calcul et affichage du nombre de lignes avec CalYear < 2020
        lines_before_2020 = self.df_incid_2018[self.df_incid_2018['CalYear'] < 2020].shape[0]
        self._print_action(f"Nombre de lignes avec CalYear < 2020 : {lines_before_2020}")

        # Filtrage des données pour l'année >= 2020
        self.df_incid_2018 = self.df_incid_2018[self.df_incid_2018['CalYear'] >= 2020]
        self._print_action("Filtrage des incidents avec année >= 2020 effectué.")
        lines_before_2020 = self.df_incid_2018[self.df_incid_2018['CalYear'] < 2020].shape[0]
        self._print_action(f"Nombre de lignes avec CalYear < 2020 après traitement : {lines_before_2020}")

    def get_data(self):
        """
        Retourne le DataFrame réduit à 30 % des lignes.        
        """
        self._print_action("Début de l'échantillonnage à 30 % des lignes.")
        
        if not hasattr(self, 'df_incid_2018'):
            raise ValueError("Les données n'ont pas encore été importées. Veuillez appeler import_data().")
        
        # Appliquer l'échantillonnage de 30 % des lignes
        df_sampled = self.df_incid_2018.sample(frac=0.30, random_state=42)
        self._print_action("Échantillonnage à 30 % effectué.")
        
        return df_sampled

    def _print_action(self, message):
        """
        Affiche un message avec l'heure d'exécution en orange.
        :param message: Le message à afficher
        """
        current_time = datetime.now().strftime("%H:%M:%S")
        print(Fore.LIGHTYELLOW_EX + f"[{current_time}] {message}" + Style.RESET_ALL)
