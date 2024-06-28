import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Datei einlesen
file_path = '1.Versuch_korrekt.CSV'  # Pfad zu deiner CSV-Datei
data = pd.read_csv(file_path, delimiter=';', decimal=',')

# Spalten zuordnen
frequenz = data['Frequenz']
ue = data['Ue']
ua = data['Ua']
phase = data['Phase']

# Verhältnis Ausgang zu Eingang in dB berechnen
verhaeltnis_db = 20 * np.log10(ua / ue)

# Bode-Diagramm erstellen
fig, ax1 = plt.subplots(figsize=(12, 6))  # Größe der Figur anpassen, z.B. 12x6 Zoll

# Erste y-Achse für das Verhältnis in dB
ax1.set_xscale('log')
ax1.set_xlabel('Frequenz / Hz')
ax1.set_ylabel('Verhältnis Ua/Ue / dB', color='tab:blue')
ax1.plot(frequenz, verhaeltnis_db, color='tab:blue', label='Verhältnis (dB)')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

# Vertikale und horizontale Linie bei 340 Hz und -3 dB hinzufügen und beschriften
ax1.axvline(x=340, color='gray', linestyle='--', label='340 Hz')
ax1.axhline(y=-3, color='gray', linestyle='--', label='-3 dB')

# Beschriftungen für die Linien auf den originalen Achsen
ax1.annotate('340 Hz', xy=(340, ax1.get_ylim()[0]), xytext=(340, ax1.get_ylim()[0] + (ax1.get_ylim()[1] - ax1.get_ylim()[0]) * 0.1),
             textcoords='data', color='gray', ha='center', va='bottom', rotation=90,
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

ax1.annotate('-3 dB', xy=(ax1.get_xlim()[0], -3), xytext=(ax1.get_xlim()[0] + (ax1.get_xlim()[1] - ax1.get_xlim()[0]) * 0.05, -3),
             textcoords='data', color='gray', ha='left', va='center',
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

# Zweite y-Achse für die Phasenverschiebung
ax2 = ax1.twinx()
ax2.set_ylabel('Phasenverschiebung / °', color='tab:red')
ax2.plot(frequenz, phase, color='tab:red', linestyle='--', label='Phase (°)')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Titel und Layout anpassen
plt.title('')
fig.tight_layout()

# Plot anzeigen
plt.show()
