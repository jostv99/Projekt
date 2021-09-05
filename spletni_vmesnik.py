import bottle
from model import *

ime_piskotka = "uporabnisko_ime"
skrivnost = "ne izdam je"


def trenutni_uporabnik():
    up_ime = bottle.request.get_cookie(ime_piskotka, secret=skrivnost)
    if up_ime:
        return Uporabnik.preberi(up_ime)
    else:
        bottle.redirect("/prijava")

@bottle.get("/")
def osnovna_stran():
    bottle.redirect("/prijava")

@bottle.get("/glavna_stran")
def glavna_stran():
    return bottle.template("osnovna_stran.html", uporabnik = trenutni_uporabnik())

@bottle.get("/prijava")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post("/prijava")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("prijava.html", napaka="Prosim vnesite uporabniško ime")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo)
        bottle.response.set_cookie(ime_piskotka, uporabnisko_ime, skrivnost, path="/")
        bottle.redirect("/glavna_stran")
    except ValueError as upsala:
        return bottle.template("prijava.html", napaka=upsala)
    
@bottle.get("/registracija")
def registracija_get():
    return bottle.template("registracija", napaka=None)

@bottle.post("/registracija")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Prosim vnesite uporabniško ime")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo)
        bottle.response.set_cookie(ime_piskotka, uporabnisko_ime, secret=skrivnost, path="/")
        bottle.redirect("/prijava")
    except ValueError as upsala:
        return bottle.template("registracija.html", napaka = upsala)

@bottle.get("/odjava")
def odjava():
    bottle.response.delete_cookie(ime_piskotka)
    bottle.redirect("/prijava")

@bottle.get("/recepti")
def recepti_get():
    vrni = []
    seznam = Recept.naredi_seznam_receptov(r"C:\Users\jostv\Documents\GitHub\Projekt") #POPRAV DA BO NORMALN DELAL
    if seznam != None:
        for (datoteka, slovar) in seznam:
            vrni.append(slovar)
    print(vrni)
    return bottle.template("rec.html", recepti = vrni)

@bottle.get("/uredi_recept")
def uredi_recept_get():
    vrni = []
    seznam = Recept.naredi_seznam_receptov(r"C:\Users\jostv\Documents\GitHub\Projekt") #POPRAV DA BO NORMALN DELAL
    if seznam != None:
        for (datoteka, slovar) in seznam:
            vrni.append(slovar)
    print(vrni)
    return bottle.template("uredi_rec.html", recepti = vrni)    


@bottle.get("/nov_recept")
def nov_recept_get():
    return bottle.template("nov_rec.html", napaka = None)

@bottle.post("/nov_recept")
def nov_recept_get():
    jed = bottle.request.forms.getunicode("jed")
    cas_priprave = bottle.request.forms.getunicode("cas_priprave")
    cas_kuhanja = bottle.request.forms.getunicode("cas_kuhanja")
    postopek = bottle.request.forms.getunicode("postopek")
    try:
        recept = Recept(jed)
        recept.nastavi_cas(cas_priprave, cas_kuhanja)
        recept.napisi_postopek(postopek)
        recept.shrani_recept()
        bottle.redirect("/glavna_stran")
    except  ValueError as upsala:
        return bottle.template("nov_rec.html", napaka = upsala)

bottle.run(debug=True, reloader=True)