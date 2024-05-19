# TODO: zaimplementować wczytywanie danych z pliku?

import numpy as np 
import matplotlib.pyplot as plt
from fuzzy_heat_air import Fuzzy
import time

# TODO: zaimplementować możliwość wyboru pożądanej temperatury
# temperatura w zakresie od -20 do 60

class FuzzyHeat(Fuzzy):
    dif = 2

    # inicjalizator odpowiedzialny za logike rozmytą
    def __init__(self, exp_temp):
        self.exp_temp = exp_temp
        super().__init__()
        
        print("co jest z toba nie tak: " + str(self.exp_temp))

        # rozmycie dla ogrzewania
        self.heat=np.zeros((5,40))
        for i in range(0,40):
            x=i*0.1
            self.heat[0,i]=x

            if x >= 0 and x <= 1:
                o_niskie = (1-x)/(1)
            else:
                o_niskie = 0

            if x >= 0.7 and x <= 1.7:
                o_srednie = (x-0.7)/(1.7-0.7)
            elif x > 1.7 and x < 2.2:
                o_srednie = 1
            elif x >= 2.2 and x <= 3.2:
                o_srednie = (3.2-x)/(3.2-2.2)
            else:
                o_srednie = 0

            if x >= 2.5 and x <= 3:
                o_wysokie = (x-2.5)/(3-2.5)
            elif x > 3 and x <= 4:
                o_wysokie = 1
            else:
                o_wysokie = 0

            self.heat[1,i] = o_niskie
            self.heat[2,i] = o_srednie
            self.heat[3,i] = o_wysokie
        
    # funkcja odpowiedzialna za wyostrzanie czyli wartość, która 
    # definiuje jak mocno powinno być ustawione ogrzewanie
    def sharp(self, user_temp = 0, out_temp = 0, real_hum = 55):
        self.user_temp = user_temp
        self.real_hum = real_hum
        self.out_temp = out_temp

        # Dodaje 200 do temperatury gdyż w linijce 8 od każdej iteracji odejmowane jest 200
        # aby zmienić zakres temperatur z +0 - +80 do -20 - +60.

        u_niska = self.temp[1,int(user_temp*10+200)]
        u_srednia = self.temp[2,int(user_temp*10+200)]
        u_wysoka = self.temp[3,int(user_temp*10+200)]

        h_niska = self.hum[1,real_hum]
        h_srednia = self.hum[2,real_hum]
        h_wysoka = self.hum[3,real_hum]

        self.inf_heat = np.zeros((5,40))
        inf = []

        # R1 IF temp = low and hum = high THEN heat = high
        # R2 IF temp = low AND hum = med THEN heat = high
        # R3 IF temp = low AND hum = low THEN heat = high

        # R4 IF temp = med AND hum = low THEN heat = med
        # R5 IF temp = med AND hum = med THEN heat = low
        # R6 IF temp = med AND hum = high THEN heat = low

        # R7 IF temp = high AND hum = low THEN heat = low
        # R8 IF temp = high AND hum = med THEN heat = low
        # R9 IF temp = high AND hum = high THEN heat = low

        R1 = min(u_niska, h_niska)
        R2 = min(u_niska, h_srednia)
        R3 = min(u_niska, h_wysoka)

        R4 = min(u_srednia, h_niska)
        R5 = min(u_srednia, h_srednia)
        R6 = min(u_srednia, h_wysoka)   

        R7 = min(u_wysoka, h_niska)
        R8 = min(u_wysoka, h_srednia)
        R9 = min(u_wysoka, h_wysoka)

        high = max(R1, R2)
        high = max(high, R3)
        # high = max(high, R4)

        med = R4

        low = max(R6, R7)
        low = max(low, R8)
        low = max(low, R9) 
        low = max(low, R5)

        for i in range(40):
            self.inf_heat[0,i] = self.heat[0,i]
            self.inf_heat[1,i] = self.heat[1,i]
            self.inf_heat[2,i] = self.heat[2,i]
            self.inf_heat[3,i] = self.heat[3,i]

            # wnioskowanie dla ogrzewania
            if(low < self.heat[1,i]):
                self.inf_heat[1,i] = low

            if(med < self.heat[2,i]):
                self.inf_heat[2,i] = med

            if(high < self.heat[3,i]): 
                self.inf_heat[3,i] = high

        # naprawione
        for i in range(40):
            a = max(self.inf_heat[1,i], self.inf_heat[2,i])
            a = max(a, self.inf_heat[3,i])

            inf.append(a)

        a = 0
        b = 0

        # naprawione
        for i in range(40):
            a = (self.inf_heat[0,i] * inf[i]) + a
            b = inf[i] + b

        # wyostrzanie
        if (abs(self.exp_temp - self.user_temp)) >= 0.1:
            wy = round((a / b),1)
        else:
            wy = 0

        if self.exp_temp < self.user_temp:
            wy = 0
        return(wy)

    def draw_chart(self):
        plt.figure(1)

        plt.subplot(411)

        plt.plot(self.temp[0,:],self.temp[1,:],'b')
        plt.plot(self.temp[0,:],self.temp[2,:],'y')
        plt.plot(self.temp[0,:],self.temp[3,:],'r')
        plt.axis([-20,59,0,1.2])
        plt.title("temperatura rozmyta")

        plt.subplot(412)

        plt.plot(self.hum[0,:],self.hum[1,:],'b')
        plt.plot(self.hum[0,:],self.hum[2,:],'y')
        plt.plot(self.hum[0,:],self.hum[3,:],'r')
        plt.axis([0,100,0,1.2])
        plt.title("wilgotnosc rozmyta")

        plt.subplot(413)

        plt.plot(self.heat[0,:],self.heat[1,:],'b')
        plt.plot(self.heat[0,:],self.heat[2,:],'y')
        plt.plot(self.heat[0,:],self.heat[3,:],'r')
        plt.axis([0,4,0,1.2])
        plt.title("rozmyta moc ogrzewania")

        # plt.subplot(414)

        # plt.plot(self.inf_heat[0,:],self.inf_heat[1,:],'b')
        # plt.plot(self.inf_heat[0,:],self.inf_heat[2,:],'y')
        # plt.plot(self.inf_heat[0,:],self.inf_heat[3,:],'r')
        # plt.axis([0,4,0,1.2])
        # plt.title("wnioskowanie dla ogrzewania")

        plt.show()


# fuzzy = FuzzyTemp()
# print(fuzzy.sharp(user_temp = 35, real_hum = 55 ))
# fuzzy.draw_chart()


