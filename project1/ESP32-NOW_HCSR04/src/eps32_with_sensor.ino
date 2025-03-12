#include <esp_now.h>
#include <WiFi.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define uS_TO_S_FACTOR 1000000 //conversione da microsecondi us a secondi s
#define TIME_TO_SLEEP  2 // [s]
#define SOUND_SPEED 0.034 //[cm/us]

RTC_DATA_ATTR int bootCount = 0; //contatore dei reboot
const int trigPin = 13; //pin D13 
const int echoPin = 12; //pin D12
long duration; //durata impulso del sensore 
float distanceCm; //[cm]
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90}; //distanza dell'ESP32
char message[10];  // Variabile per memorizzare i dati ricevuti dell'ESP32-NOW
esp_now_peer_info_t peerInfo; //struttura per memorizzare le info del peer ESP-NOW

//funzione di callback per invio di dati
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  //controllo correttezza dello stato
  //Serial.print("Send Status: ");
  //Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error");
}

//funzione di callback per ricezione dei dati
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  //copio nella variabile message i dati ricevuti e li stampo a schermo
  memcpy(&message, data, sizeof(message));
  //Serial.print("Status received: ");
  //Serial.println(message);
}

//funzione per misurare la distanza e inviare 
void measureAndSendDistance() {
  //inizializzo il segnale di trigger a low 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  //imposto il pin di trigger a un valore alto 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  //imposta infine il pin di trigger a basso
  digitalWrite(trigPin, LOW);

  //misuro il tempo che impiega il pin di echo ad alzarsi ( tempo in cui il segnale va e torna indietro)
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2; //[distanza]=[velcita]*[tempo]/2

  if (distanceCm <= 50) {
    strcpy(message, "occupied");
    Serial.println("Il parcheggio è occupato");
  } else {
    strcpy(message, "free");
    Serial.println("Il parcheggio è libero");
  }

  // invio al Mac address il valore della stringa "free" o "occupied"
  esp_now_send(broadcastAddress, (uint8_t *) &message, sizeof(message));
}

//modifica di measureandsend che conta anche quanto dura la trasmissione
void measureAndSendDistance2() {
  // Misura il tempo di inizio
  unsigned long startMeasureTime = micros();

  //inizializzo il segnale di trigger a low 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  //imposto il pin di trigger a un valore alto 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  //imposta infine il pin di trigger a basso
  digitalWrite(trigPin, LOW);

  //misuro il tempo che impiega il pin di echo ad alzarsi ( tempo in cui il segnale va e torna indietro)
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2; //[distanza]=[velcita]*[tempo]/2

  // Misura il tempo di fine
  unsigned long endMeasureTime = micros();
  unsigned long measureDuration = endMeasureTime - startMeasureTime;
  Serial.println("Durata misura sensore: " + String(measureDuration) + " microsecondi");

  // Misura il tempo di inizio della trasmissione
  unsigned long startTransmissionTime = micros();

  if (distanceCm <= 50) {
    strcpy(message, "occupied");
    Serial.println("Il parcheggio è occupato");
  } else {
    strcpy(message, "free");
    Serial.println("Il parcheggio è libero");
  }

  // invio al Mac address il valore della stringa "free" o "occupied"
  esp_now_send(broadcastAddress, (uint8_t *) &message, sizeof(message));

  // Misura il tempo di fine della trasmissione
  unsigned long endTransmissionTime = micros();
  unsigned long transmissionDuration = endTransmissionTime - startTransmissionTime;
  Serial.println("Durata trasmissione: " + String(transmissionDuration) + " microsecondi");
}

void setup() {
  //inizializzazione della comunicazione seriale
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  // Incremento del contatore di boot
  ++bootCount;
  //Serial.println("Boot number: " + String(bootCount));

  //inizializzazione di ESP-NOW e registrazione delle funzioni di callback
  esp_now_init();
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  //copio indirizzo mac in peerInfo,imposto il canale di comunicazione a 0,disabilito crittografia e aggiungo peer ESP-NOW alla lista con cui il dispositivo puo comunicare 
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);

  //configuro i pin di trigger e di echo del sensore 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Misuro e invio la distanza 
  measureAndSendDistance2();

  // Configurazione della modalità sleep
  Serial.println("Going to sleep now");
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_deep_sleep_start();
}

void loop() {
  // Lascia il loop vuoto
}