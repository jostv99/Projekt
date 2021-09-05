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

##############

@bottle.get("/")
def osnovna_stran():
    bottle.redirect("/prijava")

@bottle.get("/glavna_stran")
def glavna_stran():
    return bottle.template("osnovna_stran.html",
                            uporabnik = trenutni_uporabnik(),
                            napaka = None)

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

###############################


@bottle.get("/recepti")
def recepti_get():
    vrni = []
    seznam = Recept.naredi_seznam_receptov(os.path.dirname(os.path.abspath(__file__))) #POPRAV DA BO NORMALN DELAL
    if seznam != None:
        for (datoteka, slovar) in seznam:
            vrni.append(slovar)
    return bottle.template("rec.html", recepti = vrni)

@bottle.get("/recepti/<jed>")
def recepti_post(jed):
    seznam = Recept.naredi_seznam_receptov(os.path.dirname(os.path.abspath(__file__)))
    for (datoteka, slovar) in seznam:
        if jed in datoteka:
            return bottle.template("rec_pogled.html",
                                    jed = slovar["jed"],
                                    cas_priprave = slovar["cas_priprave"],
                                    cas_kuhanja = slovar["cas_kuhanja"],
                                    priprava = slovar["postopek"])
    else:
        return bottle.redirect("/recepti")


@bottle.get("/uredi_recept")
def uredi_recept_get():
    vrni = []
    seznam = Recept.naredi_seznam_receptov(os.path.dirname(os.path.abspath(__file__))) #POPRAV DA BO NORMALN DELAL
    if seznam != None:
        for (datoteka, slovar) in seznam:
            vrni.append(slovar)
    return bottle.template("uredi_rec.html", recepti = vrni)    

@bottle.get("/uredi_recept/<jed>")
def uredi_recept_get_jed(jed):
    seznam = Recept.naredi_seznam_receptov(os.path.dirname(os.path.abspath(__file__)))
    for (datoteka, slovar) in seznam:
        if jed in datoteka:
            return bottle.template("uredi_rec_pogled.html",
                                    jed = slovar["jed"],
                                    cas_priprave = slovar["cas_priprave"],
                                    cas_kuhanja = slovar["cas_kuhanja"],
                                    priprava = slovar["postopek"])
    else:
        return bottle.redirect("/recepti")

@bottle.post("/uredi_recept")
def uredi_recept_post():
    jed = bottle.request.forms.getunicode("ime")
    seznam = Recept.naredi_seznam_receptov(os.path.dirname(os.path.abspath(__file__)))

    s = None
    for (datoteka, slovar) in seznam:
        if jed in datoteka:
            s = slovar
    
    if s is not None:
        s["cas_priprave"] = bottle.request.forms.getunicode("cas_priprave")
        s["cas_kuhanja"] = bottle.request.forms.getunicode("cas_kuhanja")
        s["postopek"] = bottle.request.forms.getunicode("postopek")
        Recept.shrani_recept_slovar(s)
    else:
        return bottle.redirect("/recepti")


@bottle.get("/nov_recept")
def nov_recept_get():
    return bottle.template("nov_rec.html", napaka = None)

@bottle.post("/nov_recept") #popravi cas samo stevilke-drgac error, nobeno polje ne sme bit prazno
def nov_recept_get():
    jed = bottle.request.forms.getunicode("jed")
    cas_priprave = bottle.request.forms.getunicode("cas_priprave")
    cas_kuhanja = bottle.request.forms.getunicode("cas_kuhanja")
    postopek = bottle.request.forms.getunicode("postopek")
    
    if len(jed) == 0 or len(cas_priprave) == 0 or len(cas_kuhanja) == 0 or len(postopek) == 0:
        return bottle.template("nov_rec.html", napaka = "Izpolniti morate vsa polja")

    try:
        recept = Recept(jed)
        recept.nastavi_cas(int(cas_priprave), int(cas_kuhanja))
        recept.napisi_postopek(postopek)
        recept.shrani_recept()
        return bottle.template("osnovna_stran.html", uporabnik = trenutni_uporabnik(), napaka = "Recep uspešno zabeležen!")
    except  ValueError as upsala:
        return bottle.template("nov_rec.html", napaka = upsala)

@bottle.post("/izbrisi_recept/<jed>")
def izbrisi_recept(jed):
    os.remove(f"recept.{jed}.json")
    return bottle.redirect("/glavna_stran")

bottle.run(debug=True, reloader=True)