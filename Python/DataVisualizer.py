import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, Style

class DataVisualizer:
    def __init__(self, filepath):
        """
        Initialise la classe avec le chemin vers le fichier Excel.

        :param filepath: Chemin du fichier contenant les données à visualiser.
        """
        self.filepath = filepath
        self.lfb = pd.read_excel(self.filepath, engine='openpyxl')  # Chargement du fichier Excel
        # print("Colonnes disponibles :", self.lfb.columns.tolist())

    def plot_mean_attendance_per_year(self):
        """
        Affiche l'évolution du temps de réponse moyen par an.
        """
        mean_attendance_per_year = self.lfb.groupby('CallYear')['AttendanceTimeSeconds'].mean()

        plt.plot(mean_attendance_per_year.index, mean_attendance_per_year.values)
        plt.xlabel('Année')
        plt.ylabel('Temps de réponse moyen')
        plt.title("Evolution du temps de réponse moyen par an")
        plt.show()

    def plot_incident_counts_per_group(self):
        """
        Affiche un graphique des incidents traités par an et par type.
        """
        incident_counts_per_group = self.lfb.groupby(['CallYear', 'IncidentGroup'])['IncidentNumber'].count().reset_index()
        incident_counts_per_group.rename(columns={'IncidentNumber': 'IncidentCount'}, inplace=True)

        sns.barplot(data=incident_counts_per_group, x='CallYear', y='IncidentCount', hue='IncidentGroup')
        plt.xlabel('Année')
        plt.ylabel('Nombre d\'incidents')
        plt.title('Evolution du nombre d\'incidents traités par an et par type')
        plt.show()

    def plot_top_5_stations(self):
        """
        Affiche les 5 casernes avec le plus d'interventions par type d'incident.
        """
        nb_intervention_station = self.lfb.groupby("IncidentStationGround").size()
        grouped_data = self.lfb.groupby(['IncidentStationGround', 'IncidentGroup']).size().unstack(fill_value=0)

        top_5_stations = nb_intervention_station.sort_values(ascending=False).head(5).index
        grouped_data_top_5 = grouped_data.loc[top_5_stations]

        grouped_data_top_5.plot(kind='bar', stacked=True, figsize=(14, 7))

        plt.xlabel('Casernes')
        plt.ylabel('Nombre d\'interventions')
        plt.title('Top 5 des casernes avec le plus d\'interventions (par type)')
        plt.xticks(rotation=45)
        plt.legend(title='Incident Group')
        plt.show()

    def plot_least_5_stations(self):
        """
        Affiche les 5 casernes avec le moins d'interventions par type d'incident.
        """
        nb_intervention_station = self.lfb.groupby("IncidentStationGround").size()
        grouped_data = self.lfb.groupby(['IncidentStationGround', 'IncidentGroup']).size().unstack(fill_value=0)

        least_5_stations = nb_intervention_station.sort_values(ascending=True).head(5).index
        grouped_data_least_5 = grouped_data.loc[least_5_stations]

        grouped_data_least_5.plot(kind='bar', stacked=True, figsize=(14, 7))

        plt.xlabel('Casernes')
        plt.ylabel('Nombre d\'interventions')
        plt.title('Top 5 des casernes avec le moins d\'interventions (par type)')
        plt.xticks(rotation=45)
        plt.legend(title='Incident Group')
        plt.show()

    def plot_response_time_by_incident_type(self):
        """
        Affiche un diagramme en violon du temps de réponse en fonction de la nature de l'incident.
        """
        sns.violinplot(data=self.lfb, x='StopCodeDescription', y='AttendanceTimeSeconds')
        plt.title('Temps de réponse en fonction de la nature de l\'incident')
        plt.xlabel('Nature de l\'incident')
        plt.ylabel('Temps de réponse')
        plt.xticks(rotation=45)
        plt.show()

    def print_stop_code_description_counts(self):
        """
        Affiche les valeurs uniques de la colonne 'StopCodeDescription' et leur nombre d'occurrences.
        """
        print(Fore.CYAN + f"Valeurs uniques dans 'StopCodeDescription':\n{self.lfb['StopCodeDescription'].value_counts()}" + Style.RESET_ALL)

    def plot_heatmap(self):
        """
        Affiche une heatmap des corrélations entre les variables numériques du DataFrame.
        """
        # Filtrer les colonnes numériques
        df_numeric = self.lfb.select_dtypes(include=['number'])

        # Calculer et afficher la heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap des corrélations entre les variables')
        plt.show()
