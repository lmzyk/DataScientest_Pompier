import pandas as pd

class CSVHandler:
    def __init__(self, file_path):
        """
        Initialise l'instance de CSVHandler avec le chemin du fichier CSV.
        
        :param file_path: Chemin vers le fichier CSV à charger
        """
        self.file_path = file_path
        self.df = None  # DataFrame initialisé à None

    def convert_float(self, value):
        """Convertit une chaîne en float, remplaçant la virgule par un point."""
        if pd.isna(value):
            return None  # Gérer les valeurs manquantes
        try:
            return float(value.replace(',', '.'))
        except (ValueError, AttributeError):
            return None  # Retourner None si la conversion échoue

    def convert_date(self, date_str):
        """Convertit une chaîne de date au format dd-MM-yy."""
        if pd.isna(date_str):
            return None  # Gérer les valeurs manquantes
        formats = ['%d-%b-%y', '%d-%B-%y']
        date_str = date_str.replace('janv', 'jan')

        for fmt in formats:
            try:
                date_obj = pd.to_datetime(date_str, format=fmt, errors='coerce')
                return date_obj.strftime('%d-%m-%y') if pd.notna(date_obj) else None
            except ValueError:
                continue
        
        return None

    def convert_int(self, value):
        """Convertit une chaîne en int, gérant les valeurs non finies."""
        if pd.isna(value):
            return 0  # Gérer les valeurs manquantes
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0  # Retourner 0 si la conversion échoue

    def init_csv(self):
        # Charger le CSV sans spécifier de types
        self.df = pd.read_csv(self.file_path)
        columns_to_drop = ['Easting_m', 'Northing_m', 'Latitude', 'Longitude', 'Postcode_full']
        self.df.drop(columns=columns_to_drop, inplace=True)

        # Conversion manuelle des colonnes
        self.df['DateOfCall'] = self.df['DateOfCall'].apply(self.convert_date)
        self.df['CalYear'] = self.df['CalYear'].apply(self.convert_int)
        self.df['TimeOfCall'] = self.df['TimeOfCall'].astype(str)  # Conserver comme string
        self.df['HourOfCall'] = self.df['HourOfCall'].apply(self.convert_int)
        self.df['IncidentGroup'] = self.df['IncidentGroup'].astype(str)
        self.df['StopCodeDescription'] = self.df['StopCodeDescription'].astype(str)
        self.df['SpecialServiceType'] = self.df['SpecialServiceType'].astype(str)
        self.df['PropertyCategory'] = self.df['PropertyCategory'].astype(str)
        self.df['PropertyType'] = self.df['PropertyType'].astype(str)
        self.df['AddressQualifier'] = self.df['AddressQualifier'].astype(str)
        self.df['Postcode_district'] = self.df['Postcode_district'].astype(str)
        self.df['UPRN'] = self.df['UPRN'].astype(str)
        self.df['USRN'] = self.df['USRN'].astype(str)
        self.df['IncGeo_BoroughCode'] = self.df['IncGeo_BoroughCode'].astype(str)
        self.df['IncGeo_BoroughName'] = self.df['IncGeo_BoroughName'].astype(str)
        self.df['ProperCase'] = self.df['ProperCase'].astype(str)
        self.df['IncGeo_WardCode'] = self.df['IncGeo_WardCode'].astype(str)
        self.df['IncGeo_WardName'] = self.df['IncGeo_WardName'].astype(str)
        self.df['IncGeo_WardNameNew'] = self.df['IncGeo_WardNameNew'].astype(str)
        self.df['Easting_rounded'] = self.df['Easting_rounded'].apply(self.convert_float)
        self.df['Northing_rounded'] = self.df['Northing_rounded'].apply(self.convert_float)
        self.df['FRS'] = self.df['FRS'].astype(str)
        self.df['IncidentStationGround'] = self.df['IncidentStationGround'].astype(str)
        self.df['FirstPumpArriving_AttendanceTime'] = self.df['FirstPumpArriving_AttendanceTime'].apply(self.convert_int)
        self.df['FirstPumpArriving_DeployedFromStation'] = self.df['FirstPumpArriving_DeployedFromStation'].astype(str)
        self.df['SecondPumpArriving_AttendanceTime'] = self.df['SecondPumpArriving_AttendanceTime'].apply(self.convert_float)
        self.df['SecondPumpArriving_DeployedFromStation'] = self.df['SecondPumpArriving_DeployedFromStation'].apply(self.convert_float)
        self.df['NumStationsWithPumpsAttending'] = self.df['NumStationsWithPumpsAttending'].apply(self.convert_int)
        self.df['NumPumpsAttending'] = self.df['NumPumpsAttending'].apply(self.convert_int)
        self.df['PumpCount'] = self.df['PumpCount'].apply(self.convert_int)
        self.df['PumpMinutesRounded'] = self.df['PumpMinutesRounded'].apply(self.convert_int)
        self.df['Notional Cost (£)'] = self.df['Notional Cost (£)'].apply(self.convert_float)
        self.df['NumCalls'] = self.df['NumCalls'].apply(self.convert_int)

    def get_dataframe(self):
        return self.df
