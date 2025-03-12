import pandas as pd
import matplotlib.pyplot as plt

# Carica il file CSV
df1 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/project1/deep_sleep.csv')
df2 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/project1/sensor_read.csv')
df3 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/project1/transmission_power.csv')

# Estrai la colonna 'Data'
data_values1 = df1['Data']
data_values2 = df2['Data']
data_values3 = df3['Data']


# Crea una figura con 4 sottotrame
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Primo grafico
axs[0, 0].plot(data_values1, marker='o', linestyle='-', color='b')
axs[0, 0].set_title('Grafico 1')
axs[0, 0].set_xlabel('Index')
axs[0, 0].set_ylabel('Data Value')
axs[0, 0].grid(True)

# Secondo grafico
axs[0, 1].plot(data_values2, marker='x', linestyle='--', color='r')
axs[0, 1].set_title('Grafico 2')
axs[0, 1].set_xlabel('Index')
axs[0, 1].set_ylabel('Data Value')
axs[0, 1].grid(True)

# Terzo grafico
axs[1, 0].plot(data_values3, marker='s', linestyle='-.', color='g')
axs[1, 0].set_title('Grafico 3')
axs[1, 0].set_xlabel('Index')
axs[1, 0].set_ylabel('Data Value')
axs[1, 0].grid(True)



# Aggiungi spazio tra le sottotrame
plt.tight_layout()

# Mostra i grafici
plt.show()