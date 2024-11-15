import pandas as pd

class MobilisationData:
    def __init__(self, file_paths):
        self.columns_to_keep = [
            "CalYear", "HourOfCall", "DateAndTimeMobile", "DateAndTimeArrived",
            "AttendanceTimeSeconds", "TurnoutTimeSeconds", "TravelTimeSeconds",
            "DateAndTimeLeft", "DeployedFromStation_Name", "IncidentNumber",
            "DelayCode_Description"
        ]

        try:
            # Chargement des fichiers avec l'encodage approprié
            df_mobilization_2009 = pd.read_excel(file_paths[0], engine='openpyxl') 
            df_mobilization_2015 = pd.read_excel(file_paths[1], engine='openpyxl')  
            df_mobilization_2021 = pd.read_excel(file_paths[2], engine='openpyxl')
            
            # Concaténation des DataFrames
            df_mobi_combined = pd.concat([df_mobilization_2009, df_mobilization_2015, df_mobilization_2021], ignore_index=True)

            # Sélection des colonnes nécessaires
            self.df_filtered = df_mobi_combined[self.columns_to_keep]
        
        except UnicodeDecodeError as e:
            print(f"Erreur d'encodage lors du chargement des fichiers : {e}")
            raise
        except pd.errors.ParserError as e:
            print(f"Erreur lors de la lecture des fichiers CSV : {e}")
            raise
        except Exception as e:
            print(f"Une erreur est survenue lors de la lecture des fichiers : {e}")
            raise

    def get_dataframe(self):
        return self.df_filtered

    # def _load_file(self):
    #     try:
    #         # Charger les données
    #         df = pd.read_excel(self.file_path)
            
    #         # Vérifier les colonnes disponibles
    #         available_columns = [col for col in self.columns_to_keep if col in df.columns]
            
    #         if not available_columns:
    #             print(f"Erreur : Aucune des colonnes spécifiées n'est présente dans le fichier '{self.file_path}'.")
    #             return None
            
    #         # Garder uniquement les colonnes disponibles
    #         return df[available_columns]
        
    #     except Exception as e:
    #         print(f"Erreur lors du chargement des données depuis {self.file_path} : {e}")
    #         return None