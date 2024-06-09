import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import os

# Funktion zur Analyse und Plot-Erstellung
def analyze_and_plot(file_path):
    # Daten laden
    data = pd.read_csv(file_path)

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    expected_columns = ['x-axis', '1']
    data.columns = data.columns.str.strip()  # Entfernt führende und nachfolgende Leerzeichen aus den Spaltennamen

    if not all(column in data.columns for column in expected_columns):
        print(f"Die Datei {file_path} enthält nicht die erwarteten Spalten.")
        return

    # Entfernen der ersten Zeile mit den Einheiten
    data = data.drop(0).reset_index(drop=True)

    # Konvertieren der relevanten Spalten in numerische Werte
    data['x-axis'] = pd.to_numeric(data['x-axis'])
    data['1'] = pd.to_numeric(data['1'])

    # Berechnung der Peak-to-Peak-Werte
    ptp_1 = np.abs(np.max(data['1'])) + np.abs(np.min(data['1']))

    # Setzen eines höheren Schwellenwerts und einer Mindestdistanz
    threshold_1 = 0.8 * np.max(data['1'])  # 80% des maximalen Werts der ersten Kurve
    min_distance = 5000  # Mindestdistanz zwischen Maxima in Datenpunkten

    # Finden der Indizes der signifikanten Maxima mit Mindestdistanz
    peaks_1, _ = find_peaks(data['1'], height=threshold_1, distance=min_distance)

    # Maxima-Werte für die Kurve
    maxima_values_1 = data['x-axis'][peaks_1].to_numpy()

    # Berechnung der Periode T als Mittelwert der Abstände zwischen den Maxima
    if len(peaks_1) > 1:
        T_1 = np.mean(np.diff(maxima_values_1))
    else:
        T_1 = 0
    frequency_1 = 1 / T_1 if T_1 != 0 else 0

    # Initialisieren der Variablen für die zweite Kurve
    ptp_2 = None
    T_2 = None
    frequency_2 = None
    phase_shift_degrees = None
    maxima_values_2 = None

    # Überprüfen, ob Spalte '2' existiert
    if '2' in data.columns:
        data['2'] = pd.to_numeric(data['2'])
        ptp_2 = np.abs(np.max(data['2'])) + np.abs(np.min(data['2']))

        peaks_2, _ = find_peaks(data['2'], height=threshold_1, distance=min_distance)
        maxima_values_2 = data['x-axis'][peaks_2].to_numpy()

        if len(peaks_2) > 1:
            T_2 = np.mean(np.diff(maxima_values_2))
        else:
            T_2 = 0
        frequency_2 = 1 / T_2 if T_2 != 0 else 0

        if len(maxima_values_1) > 0 and len(maxima_values_2) > 0:
            time_differences = np.abs(maxima_values_1[:, np.newaxis] - maxima_values_2)
            min_time_difference = np.min(time_differences)
        else:
            min_time_difference = 0

        phase_shift_degrees = (min_time_difference / T_1) * 360 if T_1 != 0 else 0

    # Erstellen des Plots
    plt.figure(figsize=(10, 6))
    plt.plot(data['x-axis'], data['1'], linestyle='-', color='blue', label='Kurve 1')

    if '2' in data.columns:
        plt.plot(data['x-axis'], data['2'], linestyle='--', color='orange', linewidth=2, label='Kurve 2')

    # Hinzufügen der Achsenbeschriftungen
    plt.xlabel('x-axis (second)')
    plt.ylabel('Spannung (Volt)')

    # Hinzufügen eines Grids
    plt.grid(True)

    # Titel für den Plot erstellen
    title = f'Peak-to-Peak Kurve 1: {ptp_1:.2f} V'
    title += f'\nPeriode T1: {T_1:.4f} s, Frequenz f1: {frequency_1:.2f} Hz'
    
    if '2' in data.columns:
        title += f'\nPeak-to-Peak Kurve 2: {ptp_2:.2f} V'
        title += f'\nPeriode T2: {T_2:.4f} s, Frequenz f2: {frequency_2:.2f} Hz'
        title += f'\nPhasenverschiebung: {phase_shift_degrees:.2f}°'

    plt.title(title)

    # Hinzufügen einer Legende
    plt.legend()

    # Sicherstellen, dass der Hintergrund nicht schwarz ist
    plt.gca().set_facecolor('white')

    # Beschriftungen direkt auf den Kurven hinzufügen
    mid_index = len(data) // 2
    plt.annotate('Kurve 1', xy=(data['x-axis'][mid_index], data['1'][mid_index]), 
                 xytext=(data['x-axis'][mid_index], data['1'][mid_index] + 0.1),
                 arrowprops=dict(facecolor='blue', shrink=0.05),
                 horizontalalignment='left', verticalalignment='bottom')

    if '2' in data.columns:
        plt.annotate('Kurve 2', xy=(data['x-axis'][mid_index], data['2'][mid_index]), 
                     xytext=(data['x-axis'][mid_index], data['2'][mid_index] + 0.1),
                     arrowprops=dict(facecolor='orange', shrink=0.05),
                     horizontalalignment='left', verticalalignment='bottom')

    # Layout anpassen, um sicherzustellen, dass der Text nicht abgeschnitten wird
    plt.tight_layout()

    # Plot speichern
    plot_filename = os.path.splitext(os.path.basename(file_path))[0] + '.png'
    plt.savefig(plot_filename)
    plt.close()

    return maxima_values_1, maxima_values_2, T_1, T_2, frequency_1, frequency_2, phase_shift_degrees

# Durch alle CSV-Dateien im aktuellen Verzeichnis iterieren und analysieren
for file_name in os.listdir('.'):
    if file_name.endswith('.csv'):
        analyze_and_plot(file_name)
