import json
import pandas as pd
from scipy.signal import find_peaks
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:
## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        self.peaks,self.properties = self.find_peaks_ekg()
        self.estimated_hr = self.estimate_hr()
        self.fig = self.plot_time_series()

    def find_peaks_ekg(self):
        peaks, properties = find_peaks(self.df['EKG in mV'], height=330, distance=200,prominence = 60 )
        return peaks,properties
    
    def estimate_hr(self):
        self.estimated_hr_list = []
        peaks_times = self.df['Time in ms'][self.peaks]
        for i in range(1, len(peaks_times)):
            difference = (peaks_times.iloc[i] - peaks_times.iloc[i-1])/500*60
            self.estimated_hr_list.append(difference)
        self.estimated_hr = sum(self.estimated_hr_list)/len(self.estimated_hr_list)
        return self.estimated_hr

    def plot_time_series(self):
        self.fig = go.Figure()
        
        # Erstellen eines linspace von 0 bis zur Länge der Zeitdaten mit einem Abstand von 2ms
        time_values_ms = np.arange(0, len(self.df['Time in ms']) * 2, 2)
        
        # Konvertieren der Zeitwerte von Millisekunden in Sekunden
        time_values_s = time_values_ms / 1000
        
        # EKG-Signal auf der linken y-Achse
        self.fig.add_trace(go.Scatter(x=time_values_s, y=self.df['EKG in mV'], mode='lines', name='EKG Signal', yaxis='y1'))
        
        # Peaks auf der linken y-Achse
        self.fig.add_trace(go.Scatter(x=time_values_s[self.peaks], y=self.df['EKG in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10, symbol='x'), yaxis='y1'))
        
        # Geschätzte Herzfrequenz auf der rechten y-Achse
        self.fig.add_trace(go.Scatter(x=time_values_s[self.peaks], y=self.estimated_hr_list, mode='lines', name='Estimated Heartrate', yaxis='y2'))
        
        # Layout anpassen
        self.fig.update_layout(
            title='Peaks im EKG-Signal',
            xaxis_title='Zeit [s]',
            yaxis=dict(title='Amplitude [mV]', side='left', autorange=True),
            yaxis2=dict(title='Herzfrequenz [bpm]', overlaying='y', side='right', autorange=True),
            showlegend=True
        )
        return self.fig
    
    @staticmethod
    def load_by_id(id, ekg_instances):
        id_found = False
        for ekg in ekg_instances:
            if ekg.id == id:
                print({
                    "id": ekg.id,
                    "date": ekg.date,
                    "result_link": ekg.data
                })
                id_found = True
                break
        if not id_found:
            print("ID not found")


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict1 = person_data[0]["ekg_tests"][0]
    ekg_dict2 = person_data[1]["ekg_tests"][0]
    ekg_dict3 = person_data[2]["ekg_tests"][0]

    ekg1 = EKGdata(ekg_dict1)
    ekg2 = EKGdata(ekg_dict2)
    ekg3 = EKGdata(ekg_dict3)

    #ekg.load_by_id(1)
    #ekg.find_peaks()
    #ekg.estimate_hr()
    #ekg.plot_time_series()

    ekg_instances = [ekg1, ekg2, ekg3]
    EKGdata.load_by_id(4, ekg_instances)
    