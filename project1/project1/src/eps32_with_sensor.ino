#include <esp_now.h>
#include <WiFi.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define uS_TO_S_FACTOR 1000000 //conversione da microsecondi us a secondi s
#define TIME_TO_SLEEP 7 //((02 % 50) + 5) // 107184(02)
#define SOUND_SPEED 0.034 //[cm/us]
const int TRIGGER_PIN = 13; //pin D13 
const int ECHO_PIN = 12; //pin D12
long duration; //durata impulso del sensore 
float distance; //[cm]
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90}; //distanza dell'ESP32
esp_now_peer_info_t peerInfo; //struttura per memorizzare le info del peer ESP-NOW


//funzione di callback per invio di dati
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  //controllo correttezza dello stato
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error \n");
}

//funzione di callback per ricezione dei dati
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  //copio nella variabile message i dati ricevuti e li stampo a schermo
  String received_message = String((char*)data);
  Serial.print("Status received: ");
  Serial.println(received_message);
}

//funzione per misurare la distanza e inviare 
String Distance() {
  String message;
  //inizializzazione del TRIGGER PIN:
  //inizializzo TRIGGER_PIN a low per evitare sia alto dall'inizio per qualche errore e aspetto 2 microsecondi
  //imposto TRIGGER_PIN ad high per inviare impulso ultrasonico per 10 microsecondi
  //imposto TRIGGER_PIN a low per terminare l'impulso 
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  //misuro per quanto tempo ECHO_PIN rimane alto e misuro la distanza che sarà proporzionale alla durata
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * SOUND_SPEED / 2; //[distanza]=[velocita]*[tempo]/2
  //controllo che la distanza misurata sia inferiore a 50cm == parcheggio occupato da una macchina
  if (distance <= 50) {
    message = "OCCUPIED\n";
    //Serial.println("Il parcheggio è occupato");
  } else {
    message = "FREE\n";
    //Serial.println("Il parcheggio è libero");
  }
  return message;
}

//funzione per inviare messaggi e misurare la durata della trasmissione
void send_message(const uint8_t *address, const String &message) {
  esp_now_send(address, (uint8_t *)message.c_str(), message.length() + 1);
}


void print_wakeup_reason() {
  esp_sleep_wakeup_cause_t wakeup_reason;
  wakeup_reason = esp_sleep_get_wakeup_cause();
  switch (wakeup_reason) {
    case ESP_SLEEP_WAKEUP_EXT0: Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case ESP_SLEEP_WAKEUP_EXT1: Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case ESP_SLEEP_WAKEUP_TIMER: Serial.println("Wakeup caused by timer"); break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD: Serial.println("Wakeup caused by touchpad"); break;
    case ESP_SLEEP_WAKEUP_ULP: Serial.println("Wakeup caused by ULP program"); break;
    default: Serial.printf("Wakeup was not caused by deep sleep: %d\n", wakeup_reason); break;
  }
}

void setup() {
  //------------------------------------------INIZIO DEL BOOT:
  //inizializzazione della comunicazione seriale
  unsigned long boot_start = micros();
  Serial.println("start boot" + String(micros()));
  Serial.begin(115200);
  //configuro i pin di trigger e di echo del sensore 
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT); 
  //print_wakeup_reason();
  unsigned long boot_end = micros();
  unsigned long boot_duration = boot_end - boot_start;
  Serial.println("boot to measure: " + String(micros()-boot_start));
  //Serial.println("Durata boot: " + String(boot_duration) + " microsecondi");
  //----------------------------------------FINE BOOT:

  //----------------------------------------INIZIO WIFI-OFF(IDLE):
  unsigned long wifi_off_start = micros(); 
  //-----------------INIZIO SENSOR READING:
  unsigned long start_measure = micros();
  //calcolo della distanza del sensore e invio del sengale:
  String msg = Distance();
  unsigned long end_measure = micros();
  unsigned long measureDuration = end_measure - start_measure;
  Serial.println("measure to wifi off: " + String(micros()-boot_start));
  //Serial.println("Durata sensor reading: " + String(measureDuration) + " microsecondi");
  //-----------------FINE SENSOR READING.
  WiFi.mode(WIFI_STA);
  unsigned long wifi_off_end = micros();
  unsigned long wifi_off_duration = wifi_off_end - wifi_off_start;
  Serial.println("wifi off to wifi on: " + String(micros()-boot_start));
  //Serial.println("Durata wifi-off(idle): " + String(wifi_off_duration) + " microsecondi");
  //----------------------------------------FINE WIFI-OFF(IDLE).

  //----------------------------------------INIZIO WIFI-ON(TRANSMISSION):
  //inizializzazione di ESP-NOW e registrazione delle funzioni di callback
  unsigned long wifi_on_start = micros();
  esp_now_init();
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);
  //copio indirizzo mac in peerInfo,imposto il canale di comunicazione a 0,disabilito crittografia e aggiungo peer ESP-NOW alla lista con cui il dispositivo puo comunicare 
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);
  Serial.println("wifi on to sending message " + String(micros()-boot_start));
  //-----------------------INIZIO TRASMISSIONE:
  unsigned long start_transmission = micros();
  send_message(broadcastAddress, msg);
  unsigned long end_transmission = micros();
  unsigned long transmissionDuration = end_transmission - start_transmission;
  //Serial.println("Durata trasmissione: " + String(transmissionDuration) + " microsecondi");
  //----------------------FINE TRASMISSIONE.
  unsigned long wifi_on_end = micros();
  unsigned long wifi_on_duration = wifi_on_end - wifi_on_start;
  //Serial.println("Durata wifi-on: " + String(wifi_on_duration) + " microsecondi");
  Serial.println("sending message to wifi on: " + String(micros()-boot_start));
  WiFi.mode(WIFI_OFF);
  Serial.println("wifi on to deep sleep: " + String(micros()-boot_start));
  //----------------------------------------------FINE WIFI-ON

  //-----------------------------------------INIZIO MODALITA DEEP SLEEP:
  esp_sleep_enable_timer_wakeup(uS_TO_S_FACTOR*TIME_TO_SLEEP);
  Serial.println("Durata deep-sleep:" + String(TIME_TO_SLEEP) + " Seconds \n");
  Serial.flush();
  esp_deep_sleep_start();


}

void loop() {
  //loop vuoto
}