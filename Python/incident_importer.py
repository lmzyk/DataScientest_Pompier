import pandas as pd

class IncidentImporter:
    def __init__(self, incident_file_paths):
        self.incident_file_paths = incident_file_paths
        self.columns_to_keep = [
            'IncidentNumber', 'DateOfCall', 'CalYear', 'TimeOfCall', 'HourOfCall',
            'IncidentStationGround', 'NumStationsWithPumpsAttending', 'PumpCount',
            'IncidentGroup', 'StopCodeDescription', 'ProperCase', 'Notional Cost (£)',
            'Latitude', 'Longitude', 'AddressQualifier'
        ]
        
        # Chargement des fichiers avec les options appropriées
        df_incid_2009 = pd.read_csv(incident_file_paths[0])
        df_incid_2018 = pd.read_csv(incident_file_paths[1], encoding='unicode_escape', sep=';')

        # Concaténation des deux DataFrames
        df_incid_combined = pd.concat([df_incid_2009, df_incid_2018], ignore_index=True)

        self.df_filtered = df_incid_combined[self.columns_to_keep]
        
    def get_data(self):
            """
            Retourne le DataFrame combiné et réduit.
            
            :return: DataFrame combiné avec les colonnes filtrées, réduit à 30% des lignes.
            """
            if not hasattr(self, 'df_filtered'):
                raise ValueError("Les données n'ont pas encore été importées. Veuillez appeler import_data().")
            return self.df_filtered