import pandas as pd
import pickle
import os

class sportdiary():
    def __init__(self):
        """Funktion zum Erstellen des Standard-DataFrames"""
        self.table =  pd.DataFrame({
            "Wochentag": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
            "Sportart": [None, None, None, None, None, None, None],
            "Ort": [None, None, None, None, None, None, None],
            "Dauer": [None, None, None, None, None, None, None],
            "Kalorienverbrauch": [None, None, None, None, None, None, None],
            "Wetter": [None, None, None, None, None, None, None],
            "PartnerIn": [None, None, None, None, None, None, None],
        }).set_index("Wochentag")

    def load_dataframe(self,user_id):
        """Funktion zum Laden des DataFrames aus einer Datei"""
        filename = f"{user_id}_edited_df.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        else:
            return create_default_dataframe()

    def save_dataframe(df, user_id):
        """Funktion zum Speichern des DataFrames in einer Datei"""
        filename = f"{user_id}_edited_df.pkl"
        with open(filename, "wb") as file:
            pickle.dump(df, file)