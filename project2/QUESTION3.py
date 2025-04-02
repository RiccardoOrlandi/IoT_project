import pandas as pd
import re
#(ip.dst == 35.158.43.69 or ip.dst == 35.158.34.213 or ip.dst == 18.192.151.104) and mqtt and mqtt.topic contains "#"
# Percorsi dei file CSV
file_path = "pacchetti_filtrati/question3/clients_with_multilevel_wildcards_hivemq.csv"
df = pd.read_csv(file_path)

print(f"ip destination:\n{df['Destination']}")
 
# Contare il numero di righe nel DataFrame
num_righe = len(df)

# Stampare il numero di righe e il campo 'source' (ipotizzando che il campo si chiami 'source')
print(f"Numero di elementi presenti nel file: {num_righe}")
print("risposta: un solo client")


