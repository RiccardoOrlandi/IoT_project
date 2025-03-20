import math
import numpy as np

# Dati:
b = 2000  # bit
Ec = 50e-9  # nJ/bit
k = 1e-9  # nJ/bit/m²
E_tot = 5e-3  # Energia iniziale per sensore (mJ)
transmission_interval = 10 * 60  # [s]

# Posizione sink (da ottimizzare)
sink_position = np.array([20.0, 20.0]) 

# Posizione dei sensori
sensors = {
    'sensor1': (1, 2),
    'sensor2': (10, 3),
    'sensor3': (4, 8),
    'sensor4': (15, 7),
    'sensor5': (6, 1),
    'sensor6': (9, 12),
    'sensor7': (14, 4),
    'sensor8': (3, 10),
    'sensor9': (7, 7),
    'sensor10': (12, 14)
}

# Calcolo della durata per ogni sensore
def calculate_lifetime(position, sink_position, b, Ec, k, E_tot, transmission_interval):
    x, y = position
    xs, ys = sink_position
    d = math.sqrt((x - xs) ** 2 + (y - ys) ** 2)
    Etx = b * (Ec + k * d ** 2)
    n_transmission = E_tot / Etx
    lifetime = n_transmission * transmission_interval
    return lifetime

# Calcola la durata minima del sistema
lifetimes = {sensor_name: calculate_lifetime(sensor_position, sink_position, b, Ec, k, E_tot, transmission_interval) for sensor_name, sensor_position in sensors.items()}
min_lifetime = min(lifetimes.values())
print(f"Durata minima del mio sistema: {min_lifetime} secondi")
print(f"Durata minima del mio sistema: {min_lifetime / 60} minuti")


# Funzione di costo: # Restituisce la radice quadrata della somma delle distanze al quadrato
def cost_function_gradient_descent(xs, ys, sensors):
    # Calcola la somma delle distanze al quadrato (L2)
    total_distance = 0
    for sensor in sensors.values():
        x, y = sensor
        distance = math.sqrt((x - xs) ** 2 + (y - ys) ** 2)
        total_distance += distance ** 2  # L2 distance squared

    # Restituisce la radice quadrata della somma delle distanze al quadrato
    return math.sqrt(total_distance)
def gradient(xs, ys, sensors):
    grad_x = 0
    grad_y = 0
    total_distance = 0
    
    for sensor in sensors.values():
        x, y = sensor
        distance = math.sqrt((x - xs) ** 2 + (y - ys) ** 2)
        total_distance += distance ** 2
        
        # Derivata parziale rispetto a xs e ys
        grad_x += (xs - x) / distance
        grad_y += (ys - y) / distance
    
    cost = math.sqrt(total_distance)
    
    # Normalizza il gradiente
    grad_x /= cost
    grad_y /= cost
    
    return grad_x, grad_y
def gradient_descent(sensors, lr=0.01, iterations=10000):
    # Inizializza la posizione del dispositivo mobile
    xs, ys = 5, 5  # Posizione iniziale
    
    for i in range(iterations):
        # Calcola il gradiente
        grad_x, grad_y = gradient(xs, ys, sensors)
        
        # Aggiorna la posizione
        xs -= lr * grad_x
        ys -= lr * grad_y
        
        # Calcola il costo (opzionale per il monitoraggio)
        cost = cost_function_gradient_descent(xs, ys, sensors)
        if i % 100 == 0:
            print(f"Iterazione {i}, Costo: {cost}, Posizione: ({xs}, {ys})")
    
    return xs, ys



def cost_function_grid(xs, ys, sensors):
    # Calcola la distanza massima tra il dispositivo mobile e i sensori
    max_distance = 0
    for sensor in sensors.values():
        x, y = sensor
        distance = math.sqrt((x - xs) ** 2 + (y - ys) ** 2)
        max_distance = max(max_distance, distance)  # Trova la distanza massima

    return max_distance
def grid_search(sensors, grid_size=20, step=0.01):
    min_cost = float('inf')
    best_position = (None, None)
    
    # Definisci la griglia di ricerca (griglia 20x20)
    for xs in range(0, int(grid_size / step) + 1):
        for ys in range(0, int(grid_size / step) + 1):
            # Converti gli indici della griglia in coordinate reali
            real_x = xs * step
            real_y = ys * step
            cost = cost_function_grid(real_x, real_y, sensors)
            
            # Se trovi una posizione con un costo inferiore, aggiorna il miglior risultato
            if cost < min_cost:
                min_cost = cost
                best_position = (real_x, real_y)
    
    return best_position, min_cost


xs, ys = gradient_descent(sensors, lr=0.01, iterations=1000)
print(f"Posizione ottimale del dispositivo mobile con gradient descent: ({xs}, {ys})")


best_position, min_cost = grid_search(sensors, grid_size=20)
print(f"Posizione ottimale trovata con grid search: {best_position}, Costo: {min_cost}")


###########################
#Discuss the trade-offs involved in choosing a fixed sink position versus dynamically
#moving the sink. Consider the impact on system lifetime and energy consumption of each
#sensor.
