import pandas as pd
from scipy.signal import find_peaks
import plotly.graph_objects as go
import numpy as np
from tinydb import TinyDB, Query
import os
import json

class EKGdata:
    @staticmethod
    def load_ekg_data(file_path):
        def detect_file_type(file_path):
            _, file_extension = os.path.splitext(file_path)
            return file_extension.lower()

        file_extension = detect_file_type(file_path)
        
        if file_extension == ".json":
            with open(file_path) as file:
                ekg_data = json.load(file)
                for element in ekg_data:
                    dbecg.insert(element["ekg_tests"][0])

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df['Gleitender Mittelwert'] = self.df['EKG in mV'].rolling(window=5).mean()  # Berechnung des gleitenden Mittelwerts
        self.peaks, self.properties = self.find_peaks_ekg()
        self.estimated_hr = self.estimate_hr()
        self.fig = self.plot_time_series()

    def find_peaks_ekg(self):
        peaks, properties = find_peaks(self.df['EKG in mV'], height=330, distance=200, prominence=60)
        return peaks, properties
    
    def estimate_hr(self):
        self.estimated_hr_list = []
        peaks_times = self.df['Time in ms'][self.peaks]
        for i in range(1, len(peaks_times)):
            difference = (peaks_times.iloc[i] - peaks_times.iloc[i-1]) / 500 * 60
            self.estimated_hr_list.append(difference)
        self.estimated_hr = sum(self.estimated_hr_list) / len(self.estimated_hr_list)

        # Rolling Mean
        # Umwandeln der Liste in eine Pandas Serie
        self.seriestest = pd.Series(self.estimated_hr_list)
        # Berechnung des gleitenden Mittelwerts mit einem Fenster von 25
        self.rolling_mean = self.seriestest.rolling(window=25).mean()

        print(len(self.rolling_mean))
        print(len(self.estimated_hr_list))

        return self.estimated_hr

    def plot_time_series(self):
        self.fig = go.Figure()
        time_values_ms = np.arange(0, len(self.df['Time in ms']) * 2, 2)
        time_values_s = time_values_ms / 1000
        self.fig.add_trace(go.Scatter(x=time_values_s, y=self.df['EKG in mV'], mode='lines', name='EKG Signal', yaxis='y1'))
        self.fig.add_trace(go.Scatter(x=time_values_s[self.peaks], y=self.df['EKG in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10, symbol='x'), yaxis='y1'))

        # Berechnung des Mittelwerts und der dazugehörigen Zeitstempel für den Plot
        hr_time_values = time_values_s[self.peaks][1:]  # Zeitstempel der HR Werte
        self.fig.add_trace(go.Scatter(x=hr_time_values, y=self.estimated_hr_list, mode='lines', name='Estimated Heartrate', yaxis='y2'))

        # Berechnung des gleitenden Mittelwerts und der dazugehörigen Zeitstempel für den Plot
        valid_rolling_mean = self.rolling_mean.dropna()
        rolling_hr_time_values = hr_time_values[:len(valid_rolling_mean)]  # Zeitstempel für den gleitenden Mittelwert
        self.fig.add_trace(go.Scatter(x=rolling_hr_time_values, y=valid_rolling_mean, mode='lines', name='Estimated rolling Heartrate', yaxis='y2'))

        initial_zoom_start = 0
        initial_zoom_end = 10  # in Sekunden

        self.fig.update_layout(
            title='Peaks im EKG-Signal',
            xaxis_title='Zeit [s]',
            yaxis=dict(title='Amplitude [mV]', side='left', autorange=True),
            yaxis2=dict(title='Herzfrequenz [bpm]', overlaying='y', side='right', autorange=True),
            showlegend=True,
            xaxis=dict(range=[initial_zoom_start, initial_zoom_end])
        )
        self.fig.show()
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
    dbecg = TinyDB("data/EKGDatabase.json")
    dbecg.truncate()
    EKGdata.load_ekg_data("data/person_db.json")
    first_entry = dbecg.all()[0]
    EKG1 = EKGdata(first_entry)
    print(EKG1.estimated_hr)