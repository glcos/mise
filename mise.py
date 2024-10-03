import sys
from mise import mise

if len(sys.argv) < 2:
    print("Codice stazione di servizio mancante")
    print("Utilizzo: mise.py <codice>")
    print("Esempio: mise.py 15890")
    quit()

arg = sys.argv[1]
if arg.isdigit():
    station_id = int(arg)
else:
    print("Codice stazione di servizio non valido")
    quit()

class misedemo(mise):
    def logger(self, msg):
        print(msg)

mise = misedemo(station_id)

ret = mise.update()
if not ret:
    print("Errore aggiornamento dati MISE")
    quit()

print("File stazioni di servizio aggiornato al", mise.stations_ts.date())
print("File prezzi carburante aggiornato al", mise.price_ts.date())

station = mise.station
print("----Stazione di servizio----")
print(station.company)
print(station.flag)
print(station.plant_type)
print(station.name)
print(station.address)
print(station.municipality)
print(station.province)
print("latitudine", station.latitude)
print("longitudine", station.longitude)

fuels = mise.fuels
print("----Carburanti----")
for fuel in fuels:
    print(fuel.description, fuel.experience, fuel.price, fuel.timestamp)
