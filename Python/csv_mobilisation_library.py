import pandas as pd

class MobilisationData:

    def __init__(self, file_path):
        self.file_path = file_path
        self.columns_to_keep = [
            "CalYear", "HourOfCall", "DateAndTimeMobile", "DateAndTimeArrived",
            "AttendanceTimeSeconds", "TurnoutTimeSeconds", "TravelTimeSeconds",
            "DateAndTimeLeft", "DeployedFromStation_Name", "IncidentStationGround",
            "DelayCode_Description"
        ]
        self.df = self._load_file()

    def _load_file(self):
        try:
            # Charger les données
            df = pd.read_excel(self.file_path)
            
            # Vérifier les colonnes disponibles
            available_columns = [col for col in self.columns_to_keep if col in df.columns]
            
            if not available_columns:
                print(f"Erreur : Aucune des colonnes spécifiées n'est présente dans le fichier '{self.file_path}'.")
                return None
            
            # Garder uniquement les colonnes disponibles
            return df[available_columns]
        
        except Exception as e:
            print(f"Erreur lors du chargement des données depuis {self.file_path} : {e}")
            return None

    def get_dataframe(self):
        return self.df