import matplotlib.pyplot as plt
import random
import time

temperatures = []
times = []

plt.ion() # Włączenie trybu interaktywnego
fig, ax = plt.subplots()

for i in range(100):
    temperature = random.randint(0, 100)
    temperatures.append(temperature)
    times.append(i)
    ax.clear()
    ax.plot(times, temperatures)
    plt.title("Zmiana temperatury w czasie")
    plt.xlabel("Czas (s)")
    plt.ylabel("Temperatura (°C)")
    plt.pause(1) # Zatrzymaj wykres na 1 sekundę

plt.show(block=True) # Blokuj okno z wykresem do czasu zamknięcia