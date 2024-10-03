# mise
**Python library for MISE data management**

La libreria `miselib` rende disponibli i dati del sito "Osservaprezzi Carburanti" https://carburanti.mise.gov.it/ e gestisce in modo automatico
il download dei due files "prezzo_alle_8.csv" e "anagrafica_impianti_attivi.csv"

Esempio:

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

```python
csr@devl:~$ python3 misedemo.py
----Stazione di servizio----
CALOR SYSTEMS S.R.L.
MILANO REPUBBLICA
----Carburanti----
Benzina servito 2.019 02/10/2024 07:14:51
Benzina self 1.769 02/10/2024 07:14:51
Gasolio servito 1.999 02/10/2024 07:14:51
Gasolio self 1.749 02/10/2024 07:14:51
```
