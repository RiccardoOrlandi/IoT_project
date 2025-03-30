import pandas as pd

# 1. Caricare il primo file e estrarre i TKN
ack_df = pd.read_csv("pacchetti_filtrati/question1/ack.csv")
# Estrarre i token dai pacchetti con status_code >= 4.00
ack_df["status_code"] = ack_df["Info"].str.extract(r'(\d+\.\d+)').astype(float)
acks_error = ack_df[ack_df["status_code"] >= 4.00]
# Filtrare solo quelli con IP di partenza e destinazione 127.0.0.1
acks_error = acks_error[(acks_error["Source"] == "127.0.0.1") & (acks_error["Destination"] == "127.0.0.1")]
# Estrarre i token unici
acks_error_tokens = acks_error["Info"].str.extract(r'TKN:([0-9a-fA-F ]+)')[0].dropna().tolist()
unique_tokens = set(acks_error_tokens)

# 2️. Caricare il secondo file
put_df = pd.read_csv("pacchetti_filtrati/question1/confirmable_put.csv")

# Estrarre i token dal secondo file
put_df = put_df[(put_df["Source"] == "127.0.0.1") & (put_df["Destination"] == "127.0.0.1")]
put_df["tkn_found"] = put_df["Info"].str.extract(r'TKN:([0-9a-fA-F ]+)')[0]

# 3️. Contare i token presenti, evitando ripetizioni
found_tokens = set(put_df["tkn_found"].dropna())
count = len(unique_tokens.intersection(found_tokens))

# Stampare il risultato
print(f"Numero di token trovati nel secondo file (senza ripetizioni) con IP 127.0.0.1: {count}")
