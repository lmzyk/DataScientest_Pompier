import pandas as pd

class MobilisationDataMultipleFiles:
    def __init__(self, file_paths):
        self.df = self.load_and_concat_files(file_paths)

    def load_and_concat_files(self, file_paths):
        # Liste pour stocker les DataFrames
        dataframes = []
        
        # Liste des colonnes à garder
        required_columns = [
            "CalYear", "HourOfCall", "DateAndTimeMobile", "DateAndTimeArrived",
            "AttendanceTimeSeconds", "TurnoutTimeSeconds", "TravelTimeSeconds",
            "DateAndTimeLeft", "DeployedFromStation_Name", "IncidentStationGround",
            "DelayCode_Description"
        ]
        
        # Charger chaque fichier et l'ajouter à la liste
        for file_path in file_paths:
            try:
                df = pd.read_excel(file_path)
                
                # Vérification de l'existence des colonnes nécessaires
                available_columns = [col for col in required_columns if col in df.columns]
                
                # Filtrer les colonnes disponibles
                df = df[available_columns]
                
                dataframes.append(df)
            except Exception as e:
                print(f"Erreur lors du chargement des données depuis {file_path} : {e}")
        
        # Concaténer tous les DataFrames dans un seul
        if dataframes:
            concatenated_df = pd.concat(dataframes, ignore_index=True)
            return concatenated_df
        else:
            print("Erreur : Aucun fichier n'a été chargé avec succès.")
            return None

    def get_dataframe(self):
        return self.df
