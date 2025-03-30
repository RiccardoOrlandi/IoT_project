import pandas as pd

# 1. Caricare il primo file e estrarre i MID
ack_df = pd.read_csv("pacchetti_filtrati/question1/ack.csv")

# Estrarre i codici di stato dai pacchetti con status_code >= 4.00
ack_df["status_code"] = ack_df["Info"].str.extract(r'(\d+\.\d+)').astype(float)
acks_error = ack_df[ack_df["status_code"] >= 4.00]


# Filtrare solo quelli con IP di partenza e destinazione 127.0.0.1
acks_error = acks_error[(acks_error["Source"] == "127.0.0.1") & (acks_error["Destination"] == "127.0.0.1")]

# Estrarre i MID unici
acks_error_mids = acks_error["Info"].str.extract(r'MID:([0-9a-fA-F ]+)')[0].dropna().tolist()
unique_mids = set(acks_error_mids)

# 2️. Caricare il secondo file
put_df = pd.read_csv("pacchetti_filtrati/question1/confirmable_put.csv")

# Estrarre i MID dal secondo file
put_df = put_df[(put_df["Source"] == "127.0.0.1") & (put_df["Destination"] == "127.0.0.1")]
put_df["mid_found"] = put_df["Info"].str.extract(r'MID:([0-9a-fA-F ]+)')[0]

# 3️. Contare i MID presenti, evitando ripetizioni
found_mids = set(put_df["mid_found"].dropna())
count = len(unique_mids.intersection(found_mids))

# Stampare il risultato
print(f"Numero di MID trovati nel secondo file (senza ripetizioni) con IP 127.0.0.1: {count}")
