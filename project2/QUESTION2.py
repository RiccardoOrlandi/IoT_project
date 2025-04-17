#DOMANDA2:How many CoAP resources in the coap.me public server received the same number of unique Confirmable and Non Confirmable GET requests?
#TROVA PER OGNI RISORSA IL NUMERO DI CONFIRMABLE INVIATI
#ELIMINA I CONFIRMABLE CON LO STESSO TOKEN (PER OGNI RISORSA)

#TROVA PER OGNI RISORSA IL NUMERO DI NON_CONFIRMABLE GET INVIATI
#ELIMINA I CONFIRMABLE CON LO STESSO TOKEN (PER OGNI RISORSA)
#TROVA LE RISORSE(TOPIC) CHE HANNO LO STESSO NUMERO DI CONFIRMABLE E NON CONFIRMABLE

#server ip: 134.102.218.18
#coap.me

import pandas as pd
import re

# Percorsi dei file CSV
file_path1 = "pacchetti_filtrati/question2/confirmable_get.csv"
file_path2 = "pacchetti_filtrati/question2/nonconfirmable_get.csv"

# Carica i dati dai due file CSV
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

# Funzione per estrarre i topic e i token
def extract_topic_and_token(df):
    # Estrai il topic e filtra solo quelli che iniziano con "/"
    df['topic'] = df['Info'].apply(lambda info_field: info_field.split(", ")[-1] if isinstance(info_field, str) else None)
    df['topic'] = df['topic'].apply(lambda topic: topic if topic and topic.startswith('/') else None)
    
    # Filtra i messaggi validi e rimuove i valori None
    df = df[df['topic'].notna()]
    
    # Inizializza un dizionario per memorizzare i topic e i set di token unici
    topic_message_count = {}
    
    # Processa ogni riga
    for _, row in df.iterrows():
        topic = row['topic']
        info_field = row['Info']
        
        # Estrae il token (se presente)
        token_match = re.search(r"TKN:[\da-f\s]+", info_field)
        if token_match:
            token = token_match.group(0)
        else:
            token = None
        
        # Se il token è presente e il topic è valido, aggiorna il dizionario
        if token:
            if topic not in topic_message_count:
                topic_message_count[topic] = set()  # Inizializza un set per i token unici
            
            topic_message_count[topic].add(token)  # Aggiungi il token al set del topic
    
    return topic_message_count

# Estrai i topic dai due file
topic_message_count1 = extract_topic_and_token(df1)
topic_message_count2 = extract_topic_and_token(df2)

# Stampa i risultati separatamente per il primo file
print("Conteggio dei messaggi unici per ciascun topic nel primo file (confirmable.csv):")
for topic, tokens in topic_message_count1.items():
    print(f"{topic}: {len(tokens)} messaggi")

# Stampa i risultati separatamente per il secondo file
print("\nConteggio dei messaggi unici per ciascun topic nel secondo file (nonconfirmable_get.csv):")
for topic, tokens in topic_message_count2.items():
    print(f"{topic}: {len(tokens)} messaggi")

# Trova e stampa i topic che hanno lo stesso numero di messaggi nei due file
print("\nTopic con lo stesso numero di messaggi nei due file:")
for topic in topic_message_count1:
    if topic in topic_message_count2:
        if len(topic_message_count1[topic]) == len(topic_message_count2[topic]):
            print(f"{topic}: {len(topic_message_count1[topic])} messaggi")

#successivamente verifica che l'ip di destinazione sia quello di coap.me
#in questo caso sono tutti diretti all'ip del coap.me

