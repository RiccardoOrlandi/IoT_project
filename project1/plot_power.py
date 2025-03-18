import pandas as pd
import matplotlib.pyplot as plt
import os

# Carica i file CSV
df1 = pd.read_csv(os.path.join(os.getcwd(), 'project1', 'data', 'deep_sleep.csv'))
df2 = pd.read_csv(os.path.join(os.getcwd(), 'project1', 'data', 'sensor_read.csv'))
df3 = pd.read_csv(os.path.join(os.getcwd(), 'project1', 'data', 'transmission_power.csv'))

# Estrai la colonna 'Data'
data_values1 = df1['Data']
data_values2 = df2['Data']
data_values3 = df3['Data']

# Crea una figura con 4 sottotrame
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Primo grafico
axs[0, 0].plot(data_values1, marker='o', linestyle='-', color='b', markersize=6)
axs[0, 0].set_title('Grafico 1: Deep Sleep Data', fontsize=14)
axs[0, 0].set_xlabel('Index', fontsize=12)
axs[0, 0].set_ylabel('Data Value (Deep Sleep)', fontsize=12)
axs[0, 0].grid(True, linestyle='--', alpha=0.6)

# Secondo grafico
axs[0, 1].plot(data_values2, marker='x', linestyle='--', color='r', markersize=6)
axs[0, 1].set_title('Grafico 2: Sensor Readings', fontsize=14)
axs[0, 1].set_xlabel('Index', fontsize=12)
axs[0, 1].set_ylabel('Data Value (Sensor)', fontsize=12)
axs[0, 1].grid(True, linestyle='--', alpha=0.6)

# Terzo grafico
axs[1, 0].plot(data_values3, marker='s', linestyle='-.', color='g', markersize=6)
axs[1, 0].set_title('Grafico 3: Transmission Power', fontsize=14)
axs[1, 0].set_xlabel('Index', fontsize=12)
axs[1, 0].set_ylabel('Data Value (Power)', fontsize=12)
axs[1, 0].grid(True, linestyle='--', alpha=0.6)

# Rimuovi l'ultimo grafico (il quarto) se non è necessario
axs[1, 1].axis('off')

# Aggiungi spazio tra le sottotrame per migliorare la leggibilità
plt.tight_layout(pad=3.0)

# Mostra i grafici
plt.show()
