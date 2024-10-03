from mise import mise

mise = mise(15890) #15890 id stazione di servizio di esempio

ret = mise.update()
if not ret:
    print("Errore aggiornamento dati MISE")
    quit()

station = mise.station
print("----Stazione di servizio----")
print(station.company)
print(station.name)

fuels = mise.fuels
print("----Carburanti----")
for fuel in fuels:
    print(fuel.description, fuel.experience, fuel.price, fuel.timestamp)
