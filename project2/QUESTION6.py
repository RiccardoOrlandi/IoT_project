import pandas as pd
import re
#filtro: mqtt.msgtype ==3 and mqtt.qos == 0 and mqtt.retain and ip.dst == 5.196.78.28
# Percorsi dei file CSV
file_path = "pacchetti_filtrati/question6/publish_msg_qos0_retain_mosquitto.csv"
df = pd.read_csv(file_path)

#print(f"ip destination:\n{df['Destination']}")
 
# Contare il numero di righe nel DataFrame
num_righe = len(df)

# Stampare il numero di righe e il campo 'source' (ipotizzando che il campo si chiami 'source')
print(f"Numero di elementi presenti nel file: {num_righe}")
