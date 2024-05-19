import numpy as np 
import matplotlib.pyplot as plt

class Fuzzy:
    exp_temp = 0

    # zmienne dla temperatury oraz wilgotności
    user_temp = 0
    real_temp = 0
    real_hum = 0
    out_temp = 0

    # listy dla rozmytych wartości
    temp = []
    hum = []
    out_temp = []
    heat = []

    # listy dla wyostrzenia
    inf_heat = []
    inf_air = []
    inf_out = []

    inf = []
    inf_a = []
    inf_o = []

    # inicjalizator odpowiedzialny za logike rozmytą
    def __init__(self):
        # zmienna potrzebna do rozmycia
        fuzzy_exp_temp = self.exp_temp * 10

        # rozmycie dla temperatury w domu
        # i na zewnątrz
        self.temp=np.zeros((4,800))
        for i in range(0,800):
            x=i
            self.temp[0,i]=round(((x-200)*0.1),1)

            if x>=(fuzzy_exp_temp-130+200) and x<=(fuzzy_exp_temp-10+200):
                t_niska=((fuzzy_exp_temp-10+200)-x)/((fuzzy_exp_temp-10+200)-(fuzzy_exp_temp-130+200))
            elif x < (fuzzy_exp_temp-130+200):
                t_niska=1
            else:
                t_niska=0

            if x>=(fuzzy_exp_temp-130+200) and x<=(fuzzy_exp_temp-10+200):
                t_srednia=(x-(fuzzy_exp_temp-130+200))/((fuzzy_exp_temp-10+200)-(fuzzy_exp_temp-130+200))
            elif x>=(fuzzy_exp_temp-10+200) and x<=(fuzzy_exp_temp+70+200):
                t_srednia=((fuzzy_exp_temp+70+200)-x)/((fuzzy_exp_temp+70+200)-(fuzzy_exp_temp-10+200))
            else:
                t_srednia=0       

            if x>=(fuzzy_exp_temp+200) and x<=(fuzzy_exp_temp+70+200):
                t_wysoka=(x-(fuzzy_exp_temp+200))/((fuzzy_exp_temp+70+200)-(fuzzy_exp_temp+200))
            elif x<(fuzzy_exp_temp+200):
                t_wysoka=0
            else:
                t_wysoka=1
                
            self.temp[1,i] = t_niska
            self.temp[2,i] = t_srednia
            self.temp[3,i] = t_wysoka

        # Rozmycie dla wilgotności
        self.hum = np.zeros((5,101))
        for i in range(0,101):
            x=i
            self.hum[0,i]=x

            if x >= 0 and x <= 10:
                h_low = 1
            elif x > 10 and x <= 50:
                h_low = (50-x)/(50-10)
            else:
                h_low = 0

            if x >= 10 and x <= 50:
                h_med = (x-10)/(50-10)
            elif x > 50 and x < 55:
                h_med = 1
            elif x >= 55 and x <= 90:
                h_med = (90-x)/(90-55)
            else:
                h_med = 0

            if x >= 55 and x <= 90:
                h_high = (x-55)/(90-55)
            elif x > 90 and x <= 100:
                h_high = 1
            else:
                h_high = 0

            self.hum[1,i] = h_low
            self.hum[2,i] = h_med
            self.hum[3,i] = h_high


    def get_exp_temp(self):
        return self.exp_temp