import numpy as np 
import matplotlib.pyplot as plt
from fuzzy_heat_air import Fuzzy

class FuzzyAir(Fuzzy):
    def __init__(self, exp_temp):
        self.exp_temp = exp_temp
        super().__init__()

         # rozmycie dla chłodzenia
        # tak jak piec moc od 0 do 4
        self.air=np.zeros((5,40))
        for i in range(0,40):
            x=i*0.1
            self.air[0,i]=x

            if x >= 0 and x <= 1:
                c_niskie = (1-x)/(1)
            else:
                c_niskie = 0

            if x >= 0.7 and x <= 1.7:
                c_srednie = (x-0.7)/(1.7-0.7)
            elif x > 1.7 and x < 2.2:
                c_srednie = 1
            elif x >= 2.2 and x <= 3.2:
                c_srednie = (3.2-x)/(3.2-2.2)
            else:
                c_srednie = 0

            if x >= 2.5 and x <= 3:
                c_wysokie = (x-2.5)/(3-2.5)
            elif x > 3 and x <= 4:
                c_wysokie = 1
            else:
                c_wysokie = 0

            self.air[1,i] = c_niskie
            self.air[2,i] = c_srednie
            self.air[3,i] = c_wysokie

    # funkcja odpowiedzialna za wyostrzanie czyli wartość, która 
    # definiuje jak mocno powinno być ustawiona klimatyzacja
    def sharp(self, user_temp = 0, real_temp = 33, real_hum = 55):
        self.user_temp = user_temp
        self.real_temp = real_temp
        self.real_hum = real_hum

        # Dodaje 20 do temperatury gdyż w linijce 8 od każdej iteracji odejmowane jest 20
        # aby zmienić zakres temperatur z +0 - +80 do -20 - +60.

        u_niska = self.temp[1,int(user_temp*10+200)]
        u_srednia = self.temp[2,int(user_temp*10+200)]
        u_wysoka = self.temp[3,int(user_temp*10+200)]

        h_niska = self.hum[1,real_hum]
        h_srednia = self.hum[2,real_hum]
        h_wysoka = self.hum[3,real_hum]

        self.inf_air = np.zeros((5,40))
        inf_a = []

        # R1 IF temp = low and hum = high THEN air = low
        # R2 IF temp = low AND hum = med THEN air = low
        # R3 IF temp = low AND hum = low THEN air = low

        # R4 IF temp = med AND hum = low THEN air = med
        # R5 IF temp = med AND hum = med THEN air = med
        # R6 IF temp = med AND hum = high THEN air = med

        # R7 IF temp = high AND hum = low THEN air = med
        # R8 IF temp = high AND hum = med THEN air = high
        # R9 IF temp = high AND hum = high THEN air = high

        R1 = min(u_niska, h_niska)
        R2 = min(u_niska, h_srednia)
        R3 = min(u_niska, h_wysoka)

        R4 = min(u_srednia, h_niska)
        R5 = min(u_srednia, h_srednia)
        R6 = min(u_srednia, h_wysoka)   

        R7 = min(u_wysoka, h_niska)
        R8 = min(u_wysoka, h_srednia)
        R9 = min(u_wysoka, h_wysoka)

        high = max(R8, R9)

        med = max(R4,R5)
        med = max(med,R6)
        med = max(med,R7)

        low = max(R1, R2)
        low = max(low, R3)

        for i in range(40):
            self.inf_air[0,i] = self.air[0,i]
            self.inf_air[1,i] = self.air[1,i]
            self.inf_air[2,i] = self.air[2,i]
            self.inf_air[3,i] = self.air[3,i]

            # wnioskowanie dla ogrzewania
            if(low < self.air[1,i]):
                self.inf_air[1,i] = low

            if(med < self.air[2,i]):
                self.inf_air[2,i] = med

            if(high < self.air[3,i]): 
                self.inf_air[3,i] = high

        # naprawione
        for i in range(40):
            a = max(self.inf_air[1,i], self.inf_air[2,i])
            a = max(a, self.inf_air[3,i])

            inf_a.append(a)

        a = 0
        b = 0

        # naprawione
        for i in range(40):
            a = (self.inf_air[0,i] * inf_a[i]) + a
            b = inf_a[i] + b

        # wyostrzanie
        if abs(self.exp_temp - self.user_temp) >= 0.5:
            wy = round((a / b),1)
        else:
            wy = 0
        if self.exp_temp > self.user_temp:
            wy = 0

        return(wy)