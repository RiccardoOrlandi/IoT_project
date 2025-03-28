#How many different MQTT clients specify a last Will Message to be directed to a topic having as first level "university”?

#1.cerco tutti i connect command con un last_will_msg e con topic university......filtro: mqtt.msgtype == 1 && mqtt.willmsg && mqtt.willtopic contains "university
#2.+ da verificare che sia arrivato o meno????????-----in tal caso estrai id dell messagio e verifica che il suo relativo connack abbia retunr code 0


import pandas as pd
import re

# Percorsi dei file CSV
file_path = "pacchetti_filtrati/question4/connect_last_will_message_topic_univeristy.csv"
df = pd.read_csv(file_path)
# Contare il numero di righe nel DataFrame
num_righe = len(df)
print(f"Numero di elementi presenti nel file: {num_righe}")