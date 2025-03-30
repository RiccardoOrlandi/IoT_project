#How many MQTT subscribers receive a last will message derived from a subscription without a wildcard?

#1.trovo tutti i last will message inviati dai connect
#2.cerco tutti i messagi publish che hanno il contenuto dei will message 
#3.trovo i topic di questi messaggi
#4.trovo i subscriber di qusti topic che non presentano wildcard

import pandas as pd
#eseguo filtro da wireshark che ricava i publish msg con un last will msg: filter:mqtt.msg contains 65:72:72:6f:72:3a:20:61:20:56:49:50:20:43:6c:69:65:6e:74:20:6a:75:73:74:20:64:69:65:64 or mqtt.msg contains 65:72:72:6f:72:3a:20:70:65:75:69:76:64:71:6c or mqtt.msg contains 65:72:72:6f:72:3a:20:78:6c:7a:61:71:70:74:64 or mqtt.msg contains 65:72:72:6f:72:3a:20:7a:6a:7a:77:72:63:64:70
#ricavo dalla lista il nome dei topic su cui venogno inviati i last will msg: .../room1/temperature
#ricerco le subscribe request a quei determinati topic senza usare wildcard
#risposta: 3