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
    #sez -> urejeni pari (oznaka, moznost), funkcija za meni
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


def poglej_recepte(): #lahko bi zdruzu nekej funkcij skup sam zdej je kar je
    seznam_receptov = naredi_seznam_receptov()
    for indeks, recept in enumerate(seznam_receptov, 1):
        ime = recept["jed"]
        print(f"{indeks}->{ime}")
    while True:
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(seznam_receptov):
            izbrano = seznam_receptov[izbira - 1]
            prikazi_recept(izbrano)
            break
        else:
            print(f"Izberite stevilo med 1 in {len(seznam_receptov)}")        

def prikazi_recept(slovar): #dodaj dinamicen prikaz minut
    pogled = True
    jed = slovar["jed"]
    cas_priprave = str(slovar["cas_priprave"])
    cas_kuhanja = str(slovar["cas_kuhanja"])
    cas_skupni = slovar["cas_skupni"]
    postopek = str(slovar["postopek"])
    print(jed)
    print("Čas priprave: " + cas_priprave + " (min)")
    print("Čas kuhanja/pečenja: " + cas_kuhanja + " (min)")
    print("Priprava: " + postopek)
    print("\nZa nadaljevanje pritisnite \"y\"")
    while pogled:
        if input("> ") == "y":
            pogled = False
        else:
            pass
        

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

def naredi_seznam_receptov(): # seznam v katerem so slovarji!
    recepti = []
    for datoteka in os.listdir():
        if "recept" in datoteka:
            f = open(datoteka)
            slovar = json.load(f)
            recepti.append(slovar)
    return recepti




tekstovni_vmesnik()

