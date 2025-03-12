import pandas as pd

# Load the CSV file
df1 = pd.read_csv('deep_sleep.csv')
df2 = pd.read_csv('sensor_read.csv')
df3 = pd.read_csv('transmission_power.csv')

# Calculate the average power consumptions
avg_power_deep_sleep = df1['Data'].mean()
avg_power_sensor_read = df2['Data'].mean()
avg_power_transmission = df3['Data'].mean()

# Define the duration of each state (in seconds)
duration_idle = 0 
duration_transmission = 0.000297   #297 microsecondi  
duration_sensor_reading = 0.0013  #1300 microsecondi
duration_deep_sleep = 2

# Calculate the energy consumption for each state (in mJ)
energy_deep_sleep = avg_power_deep_sleep * duration_deep_sleep * 1000  
energy_sensor_reading = avg_power_sensor_read * duration_sensor_reading * 1000
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