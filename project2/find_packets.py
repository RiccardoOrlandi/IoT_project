import subprocess
from collections import Counter

# File di input pcapng
pcap_file = "challenge2.pcapng"


#QUESTION1:How many different Confirmable PUT requests obtained an unsuccessful response from the local CoAP server

#look for the ack (type=2) with some errors (code>=128) and save their message id which is the same as the confirmable

#1.find the acks with error
cmd_ack_error = f"tshark -r {pcap_file} -Y 'coap.type == 2 && coap.code >= 128' -T fields -e coap.mid"
ack_errors = subprocess.run(cmd_ack_error, shell=True, capture_output=True, text=True).stdout.splitlines()
#2.extract the message id (mid) of the confirmable with put (code 3)
cmd_put_requests = f"tshark -r {pcap_file} -Y 'coap.type == 0 && coap.code == 3' -T fields -e coap.mid"
put_requests = subprocess.run(cmd_put_requests, shell=True, capture_output=True, text=True).stdout.splitlines()
#3.print the results:
for mid in ack_errors:
    if mid in put_requests:
        print(f"ACK con errore trovato per una richiesta PUT (Message ID: {mid})")


#QUESTION2: How many CoAP resources in the coap.me public server received the same number of unique Confirmable and Non Confirmable GET requests?

#idea: find the number of confirmable e non confirmable get for each resource and then cycl to confront which has the same amount

# File di input pcapng
pcap_file = "challenge2.pcapng"

# Esegui i comandi tshark per ottenere le risorse e i token
cmd_confirmable = f"tshark -r {pcap_file} -Y 'coap.type == 0' -T fields -e coap.opt.uri_path -e coap.token"
cmd_get_nonconfirmable = f"tshark -r {pcap_file} -Y 'coap.type == 1 && coap.code == 1' -T fields -e coap.opt.uri_path -e coap.token"

# Esegui i comandi
confirmable = subprocess.run(cmd_confirmable, shell=True, capture_output=True, text=True)
get_nonconfirmable = subprocess.run(cmd_get_nonconfirmable, shell=True, capture_output=True, text=True)

# Estrai URI e Token per le richieste Confirmable
confirmable_lines = confirmable.stdout.splitlines()
unique_confirmable = set()
seen_confirmable_tokens = set()

for line in confirmable_lines:
    if '\t' in line:
        uri, token = line.split('\t')
        if token not in seen_confirmable_tokens:
            unique_confirmable.add(uri)
            seen_confirmable_tokens.add(token)

# Estrai URI e Token per le richieste Non Confirmable
get_nonconfirmable_lines = get_nonconfirmable.stdout.splitlines()
unique_get_nonconfirmable = set()
seen_nonconfirmable_tokens = set()

for line in get_nonconfirmable_lines:
    if '\t' in line:
        uri, token = line.split('\t')
        if token not in seen_nonconfirmable_tokens:
            unique_get_nonconfirmable.add(uri)
            seen_nonconfirmable_tokens.add(token)

# Conta le risorse uniche per ogni tipo di richiesta
counts_confirmable = Counter(unique_confirmable)
counts_get_nonconfirmable = Counter(unique_get_nonconfirmable)

# Trova le risorse che hanno lo stesso numero di richieste Confirmable e Non Confirmable GET con X > 0 e Y > 0
matching_resources = []

# Ciclo per confrontare i conteggi

# Ciclo per stampare la risorsa e i conteggi
for resource in counts_confirmable:
    confirmable_count = counts_confirmable[resource]
    non_confirmable_count = counts_get_nonconfirmable.get(resource, 0)
    
    #print(f"Risorsa: {resource}, Confirmable GET: {confirmable_count}, Non Confirmable GET: {non_confirmable_count}")
    
for resource in counts_confirmable:
    # Verifica se X = Y e entrambi > 0
    if confirmable_count == non_confirmable_count:
        matching_resources.append(resource)

# Risultato: risorse con lo stesso numero di richieste Confirmable e Non Confirmable GET con X > 0
print(f"Le risorse che hanno lo stesso numero di richieste Confirmable e Non Confirmable GET (con X > 0) sono: {matching_resources}")