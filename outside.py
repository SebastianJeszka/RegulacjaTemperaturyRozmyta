import numpy as np 
import matplotlib.pyplot as plt
from fuzzy_heat_air import Fuzzy

class OutTemp(Fuzzy): 

     # inicjalizator odpowiedzialny za logike rozmytą
    def __init__(self):
        super().__init__()
        
    # funkcja odpowiedzialna za wyostrzanie czyli wartość, która 
    # definiuje jak mocno powinno być ustawione ogrzewanie
    def sharp(self, out_temp = 16, in_temp = 0):
        self.out_temp = out_temp
        

        # Dodaje 200 do temperatury gdyż w linijce 8 od każdej iteracji odejmowane jest 200
        # aby zmienić zakres temperatur z +0 - +80 do -20 - +60.

        u_niska = self.temp[1,int(out_temp*10+200)]
        u_srednia = self.temp[2,int(out_temp*10+200)]
        u_wysoka = self.temp[3,int(out_temp*10+200)]

        self.inf_out = np.zeros((5,40))
        inf_o = []

        # R1 IF temp = low THEN temp = low
        # R2 IF temp = med THEN temp = med
        # R3 IF temp = high THEN temp = high


        low = u_niska
        med = u_srednia
        high = u_wysoka

        for i in range(40):
            self.inf_out[0,i] = self.out_temp[0,i]
            self.inf_out[1,i] = self.out_temp[1,i]
            self.inf_out[2,i] = self.out_temp[2,i]
            self.inf_out[3,i] = self.out_temp[3,i]

            # wnioskowanie dla ogrzewania
            if(low < self.out_temp[1,i]):
                self.inf_out[1,i] = low

            if(med < self.out_temp[2,i]):
                self.inf_out[2,i] = med

            if(high < self.out_temp[3,i]): 
                self.inf_out[3,i] = high

        # naprawione
        for i in range(40):
            a = max(self.inf_out[1,i], self.inf_out[2,i])
            a = max(a, self.inf_out[3,i])

            inf_o.append(a)

        a = 0
        b = 0

        # naprawione
        for i in range(40):
            a = (self.inf_out[0,i] * inf_o[i]) + a
            b = inf_o[i] + b

        # wyostrzanie
        if (abs(self.exp_temp - self.out_temp)) >= 0.5:
            wy = round((a / b),1)
        else:
            wy = 0
        return(wy)