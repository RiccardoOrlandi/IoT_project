import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
<<<<<<< HEAD:project1/power_estimation.py

=======
import os
>>>>>>> 5bbbd76f706bd5376284c1a35074c933a4cf23dc:project1/project1/src/power_estimation.py

Y = 8402 % 5000 + 15000 #1071(8402)

# Load the CSV file
df1 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/deep_sleep.csv')
df2 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/sensor_read.csv')
df3 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/transmission_power.csv')

#extract the data column
data_values1 = df1['Data']
data_values2 = df2['Data']
data_values3 = df3['Data']

#save the data in different structure 
boot = data_values1[(data_values1 > 350) & (data_values1 < 400)]
wifi_off = data_values1[(data_values1 > 300) & (data_values1 < 320)]
wifi_on = data_values1[(data_values1 > 700) & (data_values1 < 800)]
sensor_reading =data_values2[data_values2 > 460]
idle_sensor =data_values2[data_values2 < 340]
deep_sleep = data_values1[data_values1 < 100]
transmission = data_values3[data_values3 > 1200] #19.5dbm

avg_power_boot = boot.mean()
avg_power_wifi_off = wifi_off.mean() #IDLE
avg_power_wifi_on = wifi_on.mean()
avg_power_sensor_reading = sensor_reading.mean()
avg_power_idle_sensor = idle_sensor.mean()
avg_power_deep_sleep = deep_sleep.mean()
avg_power_transmission = transmission.mean()

# Define the duration of each state (in seconds)
duration_boot =0.000550 #[s]
duration_wifi_off = 0.201000 #[s]
duration_wifi_on = 0.001000 #[s]
duration_transmission = 0.000150 #[s] wifi.on non cosidero la distanza
duration_deep_sleep = 7.0 #[s]
duration_sensor_reading = 0.018300 #[s]

duration_active = duration_boot + duration_wifi_off + duration_wifi_on 
duration_tot = duration_active +duration_deep_sleep
duration_idle_sensor = duration_tot-duration_sensor_reading #sempre - sensor_reading

duty_cycle = (duration_active/duration_tot)*100
duty_cycle_sensor = (duration_sensor_reading/duration_idle_sensor)*100



# Calculate the energy consumption for each state (in mJ)
energy_boot = (avg_power_boot + avg_power_idle_sensor)*duration_boot*1000
energy_wifi_off = (avg_power_wifi_off + avg_power_idle_sensor)*(duration_wifi_off - duration_sensor_reading)*1000+(avg_power_sensor_reading)*duration_sensor_reading*1000
energy_wifi_on = (avg_power_wifi_on+avg_power_idle_sensor)*(duration_wifi_on-duration_transmission)*1000 +(avg_power_transmission+avg_power_idle_sensor)*(duration_transmission)*1000
energy_deep_sleep = (avg_power_deep_sleep+avg_power_idle_sensor) * duration_deep_sleep * 1000  

energy_sensor_reading = avg_power_sensor_reading*duration_sensor_reading*1000
energy_transmission = avg_power_transmission*duration_transmission*1000

# Calculate the total energy consumption for one transmission cycle (in mJ)
total_energy_consumption = (energy_boot+energy_wifi_off+energy_wifi_on+energy_deep_sleep)/1000 #[mJ]

# Print the results
print(f"Average Power Consumption during Boot: {avg_power_boot} mW")
print(f"Average Power Consumption during Idle: {avg_power_wifi_off} mW")
print(f"Average Power Consumption during Transmission: {avg_power_wifi_on} mW")
print(f"Average Power Consumption during Deep Sleep: {avg_power_deep_sleep} mW")
print(f"Total Energy Consumption for one Transmission Cycle: {total_energy_consumption} mJ")


######################## POINT 2.2(battery estimation):
#BATTERY_ENERGY:
Y = 18402 #1071(8402) [J]
number_cycle = (Y*1000)/total_energy_consumption
print(number_cycle)
total_time = number_cycle*duration_tot
print(total_time)
###########################

# Dati calcolati
avg_powers = [avg_power_boot, avg_power_wifi_off, avg_power_wifi_on, avg_power_deep_sleep]
durations = [duration_boot, duration_wifi_off, duration_wifi_on, duration_deep_sleep]
labels = ['Boot', 'Idle (WiFi Off)', 'WiFi On + Sensor Reading', 'Deep Sleep']

# Creazione del tempo cumulativo
cumulative_durations = np.cumsum([0] + durations)
time_points = np.linspace(0, cumulative_durations[-1], 1000)
power_values = np.zeros_like(time_points)

for i in range(len(durations)):
    mask = (time_points >= cumulative_durations[i]) & (time_points < cumulative_durations[i + 1])
    power_values[mask] = avg_powers[i]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(time_points, power_values, label='Power Consumption (mW)', color='blue')
plt.title('Average Power Consumption Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Power (mW)')
plt.grid(True)

# Aggiungere etichette agli intervalli
for i, label in enumerate(labels):
    plt.text((cumulative_durations[i] + cumulative_durations[i + 1]) / 2, 
             avg_powers[i] + 5, label, fontsize=10, ha='center')

plt.show()



###############################################################
#Starting from the system requirements, propose some possible
#Improvements aiming to reduce the Energy Consumption without
#modifying the main task of the parking sensor node. «Notify to a Sink
#node the occupancy state of a parking spot»

#1.dato che si tratta di un parcheggio si potrebbe modificare la potenza di trasmissione del segnale da 19.5dbm a valori inferiori 
#2.evitare idle:(switch to low 3v3 pin)il sensore rimane sempre alimentato e quindi consuma energia costanetemente, si potrebbe agigungere un interruttore in modo che si accedna solo quando wifi è on
#3.dato che il sensore produce un output binario, l'invio del messaggio potrebbe essere mandato solo in uno dei due casi e inviare ogni tot un messaggio che indica che la trasmissione è comunque on
#3.1 messaggio solo quando l'output cambia il suo stato.
#4.dato che si tratta di un parcheggio, avere come nel nostro caso un duty cycle di 7 secondi risulta troppo eccessivo e si potrebbe aumentare il deepsleep a qualche minuto.
#5.ridurre la potenza del sengale di trasmissione da 19.5dbm a 10dbm circa per poter essere in grado di raggiungere il segnale piu lontano ma evitando di sprecare energia.
#6.considerare di utilizzare la modalita light sleep 

