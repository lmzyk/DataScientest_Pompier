import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from matplotlib.colors import Normalize
import geopandas as gpd
import contextily as ctx


class IncidentMapVisualizer:
    def __init__(self, filepath):
        """
        Initialise le visualiseur avec un fichier Excel contenant les données d'incidents.
        """
        self.lfb = pd.read_excel(filepath)
        self.gdf = None
        self._prepare_data()

    def _prepare_data(self):
        """
        Prépare les données en nettoyant et en vérifiant les colonnes nécessaires.
        """
        # Renommer les colonnes si elles ont des suffixes
        if 'CalYear_x' in self.lfb.columns:
            self.lfb.rename(columns={'CalYear_x': 'CalYear'}, inplace=True)
            self.lfb.drop(columns=['CalYear_y'], inplace=True, errors='ignore')  # Supprimer CalYear_y si présent

        # Vérifier les colonnes Latitude/Longitude
        if 'Longitude' in self.lfb.columns and 'Latitude' in self.lfb.columns:
            # Création d'un GeoDataFrame pour les visualisations géographiques
            self.gdf = gpd.GeoDataFrame(
                self.lfb,
                geometry=gpd.points_from_xy(self.lfb['Longitude'], self.lfb['Latitude'])
            )
            self.gdf.set_crs(epsg=4326, inplace=True)

    def plot_points_by_attendance_time(self, cmap='coolwarm', size=20, alpha=0.6):
        """
        Affiche les points sur la carte avec des couleurs dépendant du temps d'intervention.
        """
        if 'AttendanceTimeSeconds' not in self.lfb.columns:
            print("La colonne AttendanceTimeSeconds est absente des données.")
            return

        plt.figure(figsize=(12, 8))
        norm = Normalize(vmin=self.lfb['AttendanceTimeSeconds'].min(), vmax=self.lfb['AttendanceTimeSeconds'].max())
        scatter = plt.scatter(
            self.lfb['Longitude'], 
            self.lfb['Latitude'], 
            c=self.lfb['AttendanceTimeSeconds'], 
            cmap=cmap, 
            s=size, 
            alpha=alpha,
            norm=norm
        )
        plt.colorbar(scatter, label='Temps d\'intervention (secondes)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Carte des incidents en fonction du temps d\'intervention')
        plt.grid(True)
        plt.show()

    def plot_with_basemap_and_time(self, cmap='coolwarm', alpha=0.6, size=10):
        """
        Affiche les incidents avec des couleurs basées sur le temps d'intervention et un fond de carte.
        """
        if self.gdf is not None and 'AttendanceTimeSeconds' in self.gdf.columns:
            gdf_web_mercator = self.gdf.to_crs(epsg=3857)  # Convertir au système de projection Web Mercator
            fig, ax = plt.subplots(figsize=(12, 8))
            scatter = gdf_web_mercator.plot(
                ax=ax,
                column='AttendanceTimeSeconds',
                cmap=cmap,
                markersize=size,
                alpha=alpha,
                legend=True,
                legend_kwds={'label': "Temps d'intervention (secondes)"}
            )
            ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)
            plt.title("Incidents géolocalisés avec temps d'intervention")
            plt.show()
        else:
            print("Les données géographiques ou le temps d'intervention ne sont pas disponibles.")

    def plot_heatmap(self, bins=100, cmap='viridis'):
        """
        Affiche une carte de densité des incidents.
        """
        plt.figure(figsize=(10, 6))
        plt.hist2d(
            self.lfb['Longitude'],
            self.lfb['Latitude'],
            bins=bins,
            norm=Normalize(),
            cmap=cmap
        )
        plt.colorbar(label='Densité')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Carte de densité des incidents')
        plt.show()


# Exemple d'utilisation
visualizer = IncidentMapVisualizer("C:/Users/lukas/Desktop/Git Repo/DataScientest_Pompier/df_cleaned.xlsx")

# Carte des points avec une couleur en fonction du temps d'intervention
visualizer.plot_points_by_attendance_time()

# Carte des points sur un fond géographique avec le temps d'intervention
visualizer.plot_with_basemap_and_time()
