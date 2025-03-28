import pandas as pd

# 1. Caricare il primo file e estrarre i TKN
df1 = pd.read_csv("pacchetti_filtrati/question1/ack.csv")

# Estrarre i token dai pacchetti con status_code ≥ 4.00
df1["status_code"] = df1["Info"].str.extract(r'(\d+\.\d+)').astype(float)
df_filtered1 = df1[df1["status_code"] >= 4.00]
acks_error = df_filtered1["Info"].str.extract(r'TKN:([0-9a-fA-F ]+)')[0].dropna().tolist()

# Convertire in un set per rimuovere eventuali duplicati
unique_tokens = set(acks_error)

# 2️. Caricare il secondo file
df2 = pd.read_csv("pacchetti_filtrati/question1/confirmable_put.csv")

# Estrarre i token dal secondo file
df2["tkn_found"] = df2["Info"].str.extract(r'TKN:([0-9a-fA-F ]+)')[0]

# 3️. Contare i token presenti, evitando ripetizioni
found_tokens = set(df2["tkn_found"].dropna())  # Set di token unici trovati
count = len(unique_tokens.intersection(found_tokens))  # Conta solo i match unici

# Stampare il risultato
print(f"Numero di token trovati nel secondo file (senza ripetizioni): {count}")
