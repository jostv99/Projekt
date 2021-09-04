import json

class Uporabnik:
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
            raise ValueError("Ne obstajate!") #hec, spomn se sprement
        elif uporabnik.preveri_geslo(geslo):
            return uporabnik
        else:
            raise ValueError("Napačno geslo, poskusi ponovno")

    def preveri_geslo(self, dano_geslo):
        return self.geslo == dano_geslo

class Recept:
    def __init__(self, jed):
        self.jed = jed
        self.cas_priprave = None
        self.cas_kuhanja = None
        self.cas_skupni = None
        self.sestavine = {}
        self.postopek = None

    def dodaj_sestavino(self, sestavina, kolicina, enota=None):
            self.sestavine[sestavina] = (kolicina, enota)

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
            "sestavine": self.sestavine,
            "postopek": self.postopek}


    def shrani_recept(self):
        with open(self.jed, "w") as dat:
            json.dump(self.izdelaj_slovar(), dat)