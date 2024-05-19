from tkinter import Tk, Label, Button
import tkinter as tk
from tkinter import ttk
from simulation import Simulator
from get_temp import dane

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        self.sim = Simulator()
        self.data = dane
        self.temp = tk.IntVar()
        self.exp_temp = tk.IntVar()
        self.time = tk.IntVar()
        self.season = tk.StringVar()
        self.wall = tk.IntVar()
        master.title("Piec grzewczy v0.0.1")


        self.label = Label(master, text="Wybierz jaka jest temperatura w pomieszczeniu")
        self.label.pack()

        self.combo_temp = ttk.Combobox(master, textvariable=self.temp)
        self.combo_temp['values'] = [x for x in range(40)]
        self.combo_temp['state'] = 'readonly'
        self.combo_temp.pack()

        self.label = Label(master, text="Wybierz jaka chcesz temperature")
        self.label.pack()

        self.combo_exp_temp = ttk.Combobox(master, textvariable=self.exp_temp)
        self.combo_exp_temp['values'] = [x for x in range(40)]
        self.combo_exp_temp['state'] = 'readonly'
        self.combo_exp_temp.pack()

        self.label = Label(master, text="Wybierz godzine")
        self.label.pack()

        self.combo_time = ttk.Combobox(master, textvariable=self.time)
        self.combo_time['values'] = [x for x in range(24)]
        self.combo_time['state'] = 'readonly'
        self.combo_time.pack()

        self.label = Label(master, text="Wybierz pore roku")
        self.label.pack()

        self.combo_season = ttk.Combobox(master, textvariable=self.season)
        self.combo_season['values'] = ['lato', 'zima', 'wiosna', 'jesień']
        self.combo_season['state'] = 'readonly'
        self.combo_season.pack()

        self.label = Label(master, text="Wybierz jakosc izolacji scian (im wyższa tym lepsza)")
        self.label.pack()

        self.combo_wall = ttk.Combobox(master, textvariable=self.wall)
        self.combo_wall['values'] = [1, 2, 3, 4, 5]
        self.combo_wall['state'] = 'readonly'
        self.combo_wall.pack()

        self.greet_button = Button(master, text="Run", command=lambda: self.run_chart(self.temp.get(), self.exp_temp.get(), self.season.get()))
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def run_chart(self, indoor_temp, exp_temp, season):
        # 1 argument temperatura w pomieszczeniu
        # 2 argument wilgotność w %
        # 3 argument temperatura na zewnątrz
        if season == "lato":
            self.sim.run(indoor_temp, self.data[self.time.get()][4], self.data[self.time.get()][0], exp_temp, self.wall.get())
        elif season == "zima":
            self.sim.run(indoor_temp, self.data[self.time.get()][5], self.data[self.time.get()][1], exp_temp, self.wall.get())
        elif season == "wiosna":
            self.sim.run(indoor_temp, self.data[self.time.get()][6], self.data[self.time.get()][2], exp_temp, self.wall.get())
        elif season == "lato":
            self.sim.run(indoor_temp, self.data[self.time.get()][7], self.data[self.time.get()][3], exp_temp, self.wall.get())

if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()