# mise
**Python library for MISE data management**

La libreria `miselib` rende disponibli i dati del sito "Osservaprezzi Carburanti" https://carburanti.mise.gov.it/ e gestisce in modo automatico
il download dei due files "prezzo_alle_8.csv" e "anagrafica_impianti_attivi.csv"

Esempio (misedemo.py):

```python
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
```

Risultato:

```console
csr@havm:~$ python3 misedemo.py
----Stazione di servizio----
CALOR SYSTEMS S.R.L.
MILANO REPUBBLICA
----Carburanti----
Benzina servito 2.019 02/10/2024 07:14:51
Benzina self 1.769 02/10/2024 07:14:51
Gasolio servito 1.999 02/10/2024 07:14:51
Gasolio self 1.749 02/10/2024 07:14:51
```

Esempio completo con download dei files dal sito web MISE

```console
csr@havm:~$ python3 mise.py 15890
Downloading file anagrafica_impianti_attivi.csv from MISE website
Downloading file prezzo_alle_8.csv from MISE website
File stazioni di servizio aggiornato al 2024-10-02
File prezzi carburante aggiornato al 2024-10-02
----Stazione di servizio----
CALOR SYSTEMS S.R.L.
Api-Ip
Stradale
MILANO REPUBBLICA
PIAZZA DELLA REPUBBLICA 5 20124
MILANO
MI
latitudine 45.477935609703955
longitudine 9.19595092535019
----Carburanti----
Benzina servito 2.019 02/10/2024 07:14:51
Benzina self 1.769 02/10/2024 07:14:51
Gasolio servito 1.999 02/10/2024 07:14:51
Gasolio self 1.749 02/10/2024 07:14:51
```

