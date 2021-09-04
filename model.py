import json

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo

class Recept:
    def __init__(self, jed):
        self.jed = jed
        self.cas_priprave = None
        self.cas_kuhanja = None
        self.cas_skupni = None
        self.sestavine = {}

    def dodaj_sestavino(self, sestavina, kolicina, enota=None):
            self.sestavine[sestavina] = (kolicina, enota)

    def nastavi_cas(self, priprave, kuhanja):
        #cas v min
        self.cas_priprave = priprave
        self.cas_kuhanja = kuhanja
        self.cas_skupni = kuhanja + priprave





