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
        izbira = izberi(moznosti) #bi blo bols sam preglej + dodaj, pa pr poglej se moznost uredi ampak ok, ce bo cajt

        izbira()


def poglej_recepte(): #lahko bi zdruzu nekej funkcij skup sam zdej je kar je
    seznam_receptov = naredi_seznam_receptov()
    for indeks, (_, recept) in enumerate(seznam_receptov, 1):
        ime = recept["jed"]
        print(f"{indeks}->{ime}")
    while True:
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(seznam_receptov):
            izbrano = seznam_receptov[izbira - 1][1]
            pogled = True
            prikazi_recept(izbrano)
            print("\nZa nadaljevanje pritisnite \"y\"")
            while pogled:
                if input("> ") == "y":
                    pogled = False
            else:
                pass
            break
        else:
            print(f"Izberite stevilo med 1 in {len(seznam_receptov)}")        


def prikazi_recept(slovar): #dodaj dinamicen prikaz minut, moznost komentarja?
    jed = slovar["jed"]
    cas_priprave = str(slovar["cas_priprave"])
    cas_kuhanja = str(slovar["cas_kuhanja"])
    cas_skupni = slovar["cas_skupni"]
    postopek = str(slovar["postopek"])
    print("%"*14)
    print(jed)
    print("Čas priprave: " + cas_priprave + " (min)")
    print("Čas kuhanja/pečenja: " + cas_kuhanja + " (min)")
    print("Priprava: " + postopek)
    print("%"*14)

        

def nov_recept(): #dodaj - ime uporabnika k je dodal
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
    seznam_receptov = naredi_seznam_receptov()
    for indeks, (datoteka, recept) in enumerate(seznam_receptov, 1):
        ime = recept["jed"]
        print(f"{indeks}->{ime}")
    while True: #again ista funkcija k za pregled pac res bi loh skrcu use skp
        izbira = vnesi_stevilo("> ")
        if 1 <= izbira <= len(seznam_receptov):
            izbrano = seznam_receptov[izbira - 1]
            uredi(izbrano)
            break
        else:
            print(f"Izberite stevilo med 1 in {len(seznam_receptov)}") 


def uredi(izbrano):
    dat = izbrano[0]
    sez = izbrano[1]
    while True:
        prikazi_recept(sez)
        print("Kaj želite urediti?")
        print("1->Čas priprave")
        print("2->Čas kuhanja/pečenja")
        print("3->Pripravo")
        print("4->Nazaj")
        izbira = vnesi_stevilo("> ")
        if izbira == 1:
            print("Kaj želite da je nov čas priprave?")
            sez["cas_priprave"] = vnesi_stevilo("> ")
        elif izbira == 2:
            print("Kaj želite da je nov čas kuhanja/pečenja?")
            sez["cas_kuhanja"] = vnesi_stevilo("> ")
        elif izbira == 3:
            print("Napišite nov postopek priprave")
            sez["postopek"] = input("> ")
        elif izbira == 4:
            return None
        else:
            print("Izberite število med 1 in 4")
        with open(dat, "w") as jf:
            json.dump(sez, jf)


def naredi_seznam_receptov(): # seznam v katerem so slovarji!
    recepti = []
    for datoteka in os.listdir():
        if "recept" in datoteka:
            f = open(datoteka)
            slovar = json.load(f)
            recepti.append((datoteka, slovar))
    return recepti
    # zamenjej z metodo na razredu (za zdej dela tko da sam pust)



tekstovni_vmesnik()

