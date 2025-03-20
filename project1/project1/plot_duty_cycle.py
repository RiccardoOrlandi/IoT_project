import matplotlib.pyplot as plt
import numpy as np

# Define the data
phases = ['deep sleep','boot', 'measuring', 'turning wifi on', 'setting up connection', 'transmission', 'deep sleep']
durations = [0.1,0.00095, 0.0025, 0.182897, 0.000505, 0.00041, 0.1]
powers = [59.66, 367.1, 466.7, 310.9, 775.5, 1222, 59.66]

# Create time axis
time = []
power = []

# Create the graph data by repeating power values over the respective durations
current_time = 0
for i in range(len(phases)):
    phase_time = np.linspace(current_time, current_time + durations[i], 100)
    phase_power = np.full_like(phase_time, powers[i])
    time.extend(phase_time)
    power.extend(phase_power)
    current_time += durations[i]

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(time, power, label='Power Consumption', color='b')
plt.xlabel('Time [s]')
plt.ylabel('Power [mW]')
plt.title('Power Consumption over Time')
plt.grid(True)
plt.legend()
plt.show()
