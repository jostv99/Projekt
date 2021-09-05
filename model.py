import json
import os

class Uporabnik: ####DODAJ ZAKAJ SE TI NE USPE PRIJAVIT, REGISTRIRAT KER ZDEJ SAM NIMAS POJMA KAJMA
    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo

    def izdelaj_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "geslo": self.geslo,
        }

    @staticmethod
    def preberi_slovar(slovar):
        up_ime = slovar["uporabnisko_ime"]
        geslo = slovar["geslo"]
        return Uporabnik(up_ime, geslo)

    @staticmethod
    def uporabnikova_datoteka(ime):
        return f"{ime}.json"

    def shrani(self):
        with open(Uporabnik.uporabnikova_datoteka(self.uporabnisko_ime), "w") as dat:
            json.dump(self.izdelaj_slovar(), dat)

    @staticmethod
    def registracija(up_ime, geslo):
        if Uporabnik.preberi(up_ime) is not None:
            raise ValueError("Že obstajate") #dej to tut spremen
        elif "recept" in up_ime:
            raise ValueError("Ime ne sme vsebovati besede \"recept\"")
        else:
            uporabnik = Uporabnik(up_ime, geslo)
            uporabnik.shrani()
            return uporabnik

    @staticmethod
    def preberi(up_ime):
        try:
            with open(Uporabnik.uporabnikova_datoteka(up_ime)) as dat:
                slovar = json.load(dat)
                return Uporabnik.preberi_slovar(slovar)
        except FileNotFoundError:
            return None

    @staticmethod
    def prijava(up_ime, geslo):
        uporabnik = Uporabnik.preberi(up_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime in geslo se ne ujemata") #hec, spomn se sprement
        elif uporabnik.preveri_geslo(geslo):
            return uporabnik
        else:
            raise ValueError("Napačno geslo, poskusi ponovno")

    def preveri_geslo(self, dano_geslo):
        return self.geslo == dano_geslo



 




class Recept:
    def __init__(self, jed):
        self.jed = str(jed)
        self.cas_priprave = None
        self.cas_kuhanja = None
        self.cas_skupni = None
        self.postopek = None


    def nastavi_cas(self, priprave, kuhanja):
        #cas v min
        self.cas_priprave = priprave
        self.cas_kuhanja = kuhanja
        self.cas_skupni = kuhanja + priprave

    def napisi_postopek(self, tekst):
        self.postopek = tekst

    def izdelaj_slovar(self):
        return {
            "jed": self.jed,
            "cas_priprave": self.cas_priprave,
            "cas_kuhanja": self.cas_kuhanja,
            "cas_skupni": self.cas_skupni,
            "postopek": self.postopek}


    def shrani_recept(self):
        with open("recept." + self.jed + ".json", "w") as dat:
            json.dump(self.izdelaj_slovar(), dat)

    @staticmethod
    def nalozi_recept(datoteka):
        try:
            with open(datoteka) as dat:
                slovar = json.load(dat)
                jed = slovar["jed"]
                cas_priprave = slovar["cas_priprave"]
                cas_kuhanja = slovar["cas_kuhanja"]
                cas_skupni = slovar["cas_skupni"]
                postopek = slovar["postopek"]
        except FileNotFoundError:
            return None

    @staticmethod
    def naredi_seznam_receptov(pot):
        try:
            recepti = []
            for datoteka in os.listdir(pot):
                if "recept" in datoteka:
                    f = open(datoteka)
                    slovar = json.load(f)
                    recepti.append((datoteka, slovar))
            return recepti

        except FileNotFoundError:
            return None