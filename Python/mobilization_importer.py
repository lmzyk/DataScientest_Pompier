import pandas as pd
from colorama import Fore, Style
from datetime import datetime

class MobilisationImporter:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.columns_to_keep = [
            "CalYear", "HourOfCall", "DateAndTimeMobile", "DateAndTimeArrived",
            "AttendanceTimeSeconds", "TurnoutTimeSeconds", "TravelTimeSeconds",
            "DateAndTimeLeft", "DeployedFromStation_Name", "IncidentNumber",
            "DelayCode_Description"
        ]
        self.df_filtered = None

        # Heure de début de l'importation
        start_time = datetime.now()
        self.print_with_time("### Début de l'importation des mobilisations ###", start_time)

        try:
            # Chargement et concaténation des fichiers Excel
            self.print_with_time(f"Chargement des fichiers : {file_paths[0]} et {file_paths[1]}")
            df_mobilization_2015 = pd.read_excel(file_paths[0], engine='openpyxl')
            df_mobilization_2021 = pd.read_excel(file_paths[1], engine='openpyxl')

            # Concaténation des deux fichiers
            df_mobi_combined = pd.concat([df_mobilization_2015, df_mobilization_2021], ignore_index=True)
            self.print_with_time(f"Concaténation des fichiers réussie. Nombre total de lignes : {len(df_mobi_combined)}")

            # Vérification de la présence des colonnes nécessaires
            missing_columns = [col for col in self.columns_to_keep if col not in df_mobi_combined.columns]
            if missing_columns:
                raise ValueError(f"Les colonnes suivantes sont absentes : {', '.join(missing_columns)}")

            # Filtrage des colonnes et des années >= 2020
            self.print_with_time("Filtrage des colonnes et des années >= 2020")
            self.df_filtered = df_mobi_combined[self.columns_to_keep]
            self.df_filtered = self.df_filtered[self.df_filtered['CalYear'] >= 2020]

            # Afficher le nombre de lignes après filtrage
            self.print_with_time(f"Nombre de lignes après filtrage : {len(self.df_filtered)}")

        except UnicodeDecodeError as e:
            self.print_with_time(f"Erreur d'encodage lors du chargement des fichiers : {e}", error=True)
            raise
        except pd.errors.ParserError as e:
            self.print_with_time(f"Erreur lors de la lecture des fichiers Excel : {e}", error=True)
            raise
        except Exception as e:
            self.print_with_time(f"Une erreur est survenue lors de la lecture des fichiers : {e}", error=True)
            raise
        finally:
            end_time = datetime.now()
            self.print_with_time("### Fin de l'importation des mobilisations ###", end_time)
            self.print_duration(start_time, end_time)

    def get_dataframe(self):
        """
        Retourne le DataFrame filtré.
        """
        if self.df_filtered is None:
            raise ValueError("Les données n'ont pas été importées correctement.")
        return self.df_filtered

    @staticmethod
    def print_with_time(message, current_time=None, error=False):
        """
        Affiche un message avec l'heure actuelle en orange ou en rouge en cas d'erreur.
        """
        if current_time is None:
            current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        color = Fore.RED if error else Fore.YELLOW
        print(color + f"{time_str} - {message}" + Style.RESET_ALL)

    @staticmethod
    def print_duration(start_time, end_time):
        """
        Affiche la durée totale du traitement.
        """
        duration = end_time - start_time
        print(Fore.LIGHTMAGENTA_EX + f"Durée totale : {duration}" + Style.RESET_ALL)
