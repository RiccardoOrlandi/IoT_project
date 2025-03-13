import pandas as pd

# Load the CSV file
df1 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/deep_sleep.csv')
df2 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/sensor_read.csv')
df3 = pd.read_csv('/Users/riccardoorlandi/Desktop/universita/5anno/2semestre/INTERNET_OF_THINGS/projects/IoT_project/project1/data/transmission_power.csv')

#extract the data column
data_values1 = df1['Data']
data_values2 = df2['Data']
data_values3 = df3['Data']

#save the data in different structure 
deep_sleep = data_values1[data_values1 < 100]
wifi_off = data_values1[(data_values1 > 300) & (data_values1 < 320)]
wifi_on = data_values1[(data_values1 > 700) & (data_values1 < 800)]
boot = data_values1[(data_values1 > 350) & (data_values1 < 400)]
sensor_reading =data_values2[data_values2 > 460]
idle =data_values2[data_values2 < 340]

avg_power_deep_sleep = deep_sleep.mean()
avg_power_wifi_off = wifi_off.mean()
avg_power_wifi_on = wifi_on.mean()
avg_power_boot = boot.mean()
avg_power_sensor_reading = sensor_reading.mean()
avg_power_idle = idle.mean()


# Define the duration of each state (in seconds)
duration_boot = 
duration_transmission = 0.000297   #305 microsecondi  
duration_sensor_reading = 0.0013  #1300 microsecondi
duration_deep_sleep = 2 
duration_idle = 0 
# Calculate the energy consumption for each state (in mJ)
energy_deep_sleep = avg_power_deep_sleep * duration_deep_sleep * 1000  
energy_sensor_reading = avg_power_sensor_reading * duration_sensor_reading * 1000
energy_transmission = avg_power_transmission * duration_transmission * 1000

# Calculate the total energy consumption for one transmission cycle (in mJ)
total_energy_consumption = energy_deep_sleep + energy_transmission + energy_sensor_reading

# Print the results
print(f"Average Power Consumption during Deep Sleep: {avg_power_deep_sleep} mW")
print(f"Energy Consumption during Deep Sleep: {energy_deep_sleep} mJ")
#print(f"Energy Consumption during Idle: {energy_idle} mJ")
print(f"Energy Consumption during Transmission: {energy_transmission} mJ")
print(f"Energy Consumption during Sensor Reading: {energy_sensor_reading} mJ")
print(f"Total Energy Consumption for one Transmission Cycle: {total_energy_consumption} mJ")