#DOMANDA3:How many different MQTT clients subscribe to the public broker HiveMQ using multi-level wildcards?

#CERCA TUTTE LE SUBSCRIBE REQUEST EFFETTUATE 
#FILTRA SOLO QUELLE IN CUI VI SONO LE WILDCARDS
#FILTRA SOLO QUELLE RELATIVE A HIVEMQ
#filtro:(ip.dst == 34.158.43.69 or ip.dst == 35.158.34.213 || ip.dst == 18.192.151.104) && mqtt.msgtype == 8 && mqtt.topic contains "#"

import pandas as pd
import re

# Percorsi dei file CSV
file_path = "pacchetti_filtrati/question3/clients_with_multilevel_wildcards_hivemq.csv"
df = pd.read_csv(file_path)
# Contare il numero di righe nel DataFrame
num_righe = len(df)
print(f"Numero di elementi presenti nel file: {num_righe}")