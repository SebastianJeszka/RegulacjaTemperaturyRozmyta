from heat import FuzzyHeat
from air import FuzzyAir
from outside import OutTemp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

class Simulator:
    
    def __init__(self):
        self.temp = 0
        self.hum = 0
        self.furnance_power = 1
        self.clim_power = 1
        self.dif = 0
        self.dif_2 = 0
        # izolacja sciany im mniejsza wartosc tym bardziej "ucieka / dostaje sie cieplo"
        self.wall = 0

        
        self.temperatures = [] # temperatury
        self.times = [] # co jaki czas mierzona jest temperatura
        

    def run(self, temp, hum, out_temp, exp_temp, wall):
        self.exp_temp = exp_temp
        self.ft = FuzzyHeat(self.exp_temp)
        self.at = FuzzyAir(self.exp_temp)
        plt.ion() # tryb interaktywnego wykresu
        self.fig, self.ax = plt.subplots()
        self.temp = temp
        self.hum = hum
        self.wall = wall
        
        
        for i in range(20):
            print(self.temp)
            heat_power = self.ft.sharp(user_temp = self.temp, real_hum = self.hum)
            air_power = self.at.sharp(user_temp = self.temp, real_hum = self.hum)
            self.dif = exp_temp - self.temp
            self.dif_2 = self.temp - out_temp
            print("roznica temperatur w pokoju i oczekiwanego: " + str(self.dif))
            
            if self.dif > 20:
                self.furnance_power = 3
            elif self.dif >= 15 and self.dif < 20:
                self.furnance_power = 2.5
            elif self.dif >= 10 and self.dif < 15:
                self.furnance_power = 2
            elif self.dif >= 5 and self.dif < 10:
                self.furnance_power = 1.5
            elif self.dif <= 5 and self.dif > 0:
                self.furnance_power = 1

            if self.dif < -20:
                self.clim_power = 3
            elif self.dif <= -20 and self.dif > -15:
                self.clim_power = 2.5
            elif self.dif <= -15 and self.dif > -10:
                self.clim_power = 2
            elif self.dif <= -10 and self.dif > -5:
                self.clim_power = 1.5
            elif self.dif > -5 and self.dif <= 0:
                self.clim_power = 1
            
            grzanie = round((heat_power * self.furnance_power),1)
            klima = round((air_power * self.clim_power),1)
            zmiana_out = round((self.dif_2/(self.wall * 10)),1)

            print("moc pieca: " + str(self.furnance_power))
            print("zmiana temperatury grzanie: " + str(grzanie))
            print("zmiana temperatury klima: " + str(klima))
            print("zmiana temperatury temp na zewnątrz: " + str(zmiana_out))
            if self.dif > 0:
                self.temp = round((self.temp + grzanie - klima - zmiana_out),1)
            elif self.dif <= 0:
                self.temp = round((self.temp + grzanie - klima + zmiana_out),1)
            # else:
            #     self.temp = round(self.temp + round((heat_power * self.furnance_power),1) - (round((air_power * self.clim_power) + round(self.dif/3,1),1)/2))
            self.hum = self.hum + int(heat_power + 2)
            # wyostrzenie dla wilgoci
            if self.hum >= 70:
                self.hum = 70

            print(f"temperatura {i} iteracji wynosi: " + str(self.temp))
            print("wyostrzanie dla temperatury: " + str(self.ft.sharp(user_temp = self.temp, real_hum = self.hum)))
            print("wyostrzanie dla klimy: " + str(self.at.sharp(user_temp = self.temp, real_hum = self.hum)))

            self.temperatures.append(self.temp)

            self.update_plot(i)


        
        plt.show(block = True)


    def update_plot(self, i):
        self.times.append(i) # dodaj jednostke czasu
        self.ax.clear()
        self.ax.plot(self.times, self.temperatures)
        plt.title("Zmiana temperatury w czasie")
        plt.xlabel("Czas (s)")
        plt.ylabel("Temperatura (°C)")
        plt.pause(1)



    # sim = Simulator()
    
    
    
    

