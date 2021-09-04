from model import *

###########

def uvod():
    print("Za izhod vnesite \"q\"")
    print("Prosim izberite kaj želite narediti")

def vnesi_stevilo(kako):
    while True:
        try:
            stevilo = input(kako)
            if stevilo == "q":
                exit()
            else:
                return int(stevilo)
        except ValueError:
            print("Vaša izbira ni vredu, poskusite ponovno")

def izberi(sez):
    #sez -> urejeni pari (oznaka, moznost)
    for indeks, (oznaka, _) in enumerate(sez, 1):
        print(f"{indeks}->{oznaka}")
    while True:
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(sez):
            _, izbrano = sez[izbira - 1]
            return izbrano
        else:
            print(f"Izberite stevilo med 1 in {len(sez)}")


############# 

def tekstovni_vmesnik():
    uvod()
    while True: #funkcija izpisi_moznosti? samo da ni prevec druga stvar..
        moznosti = [
            ("Poglej recepte", poglej_recepte),
            ("Dodaj nov recept", nov_recept),
            ("Uredi star recept", uredi_recept)
        ]
        izbira = izberi(moznosti)

        izbira()


def poglej_recepte():
    recepti_seznam_slovarjev = []
    recepti = {}
    with os.scandir() as datoteke:
        for datoteka in datoteke:
            print(datoteka)
            if "recept" in str(datoteka.name):
                slovar = json.loads(datoteka)
                recepti_seznam_slovarjev.append(slovar)
            else:
                pass
    print(recepti_seznam_slovarjev)


def nov_recept():
    print("Napišite ime jedi:") #popravi, lahko je vec istih imen pa bo problem
    ime = input("> ")
    recept = Recept(ime)
    print("Koliko časa (min) traja priprava (brez kuhanja/pečenja)?")
    cas1 = None
    while cas1 == None:
        try:
            cas1 = int(input("> "))
        except ValueError:
            print("Vnos ni pravilen, prosim probajte ponovno")

    print("Koliko časa (min) se jed kuha/peče?")
    cas2 = None
    while cas2 == None:
        try:
            cas2 = int(input("> "))
        except ValueError:
            print("Vnos ni pravilen, prosim probajte ponovno")

    recept.nastavi_cas(cas1,cas2)
    print("Napišite kratek opis priprave jedi")
    opis = input("> ")
    recept.napisi_postopek(opis)
    recept.shrani_recept()

def uredi_recept():
    pass




tekstovni_vmesnik()

