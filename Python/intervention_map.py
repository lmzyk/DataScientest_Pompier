import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import contextily as ctx
from shapely.geometry import Point
from matplotlib.colors import Normalize
from matplotlib import cm

class InterventionMap:
    def __init__(self, df):
        self.df = df
        # Créer un GeoDataFrame à partir du DataFrame pandas
        self.gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_xy(df['Longitude'], df['Latitude']))
        self.gdf.crs = 'EPSG:4326'  # Assurer que les coordonnées sont en WGS84 (latitude/longitude)

    def plot_intervention_map(self):
        # Créer un dégradé de couleurs basé sur la colonne 'AttendanceTimeSeconds'
        norm = Normalize(vmin=self.df['AttendanceTimeSeconds'].min(), vmax=self.df['AttendanceTimeSeconds'].max())
        cmap = cm.viridis  # Choix du colormap (tu peux essayer d'autres comme 'plasma', 'inferno', etc.)

        # Tracer la carte
        fig, ax = plt.subplots(figsize=(10, 10))

        # Tracer la carte de fond OpenStreetMap en utilisant contextily
        self.gdf.to_crs(epsg=3857, inplace=True)  # Convertir en projection Web Mercator (EPSG:3857)
        ax.set_axis_off()  # Retirer l'axe pour ne pas afficher les coordonnées
        self.gdf.plot(ax=ax, marker='o', color='red', markersize=5, alpha=0.7)  # Placer les points des interventions
        ctx.add_basemap(ax, crs=self.gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)  # Ajouter la carte de fond

        # Appliquer le dégradé de couleurs en fonction du temps d'intervention
        sc = ax.scatter(self.df['Longitude'], self.df['Latitude'], c=self.df['AttendanceTimeSeconds'], cmap=cmap, norm=norm, s=30, alpha=0.7)

        # Ajouter une barre de couleurs
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Temps d\'intervention (en secondes)')

        # Ajouter des titres et labels
        ax.set_title("Carte des interventions à Londres", fontsize=15)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Afficher la carte
        plt.show()