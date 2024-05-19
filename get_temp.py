import pyexcel

# Wczytanie danych z pliku .ods
book = pyexcel.get_book(file_name="temperatures.xls")
sheet = book[0] # Wybierz pierwszy arkusz

data = []
datas = []


# Iteruj przez wszystkie wiersze w arkuszu
for row in sheet:
    for item in row:
        # Sprawdzenie, czy komórka zawiera liczbę
        if type(item) == int or type(item) == float:
            datas.append(item)
    data.append(datas)
    datas = []

del(data[0])

dane = data