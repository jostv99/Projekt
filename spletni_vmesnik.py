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

@bottle.get("/glavna-stran")
def glavna_stran():
    return bottle.template("osnovna_stran.html")

@bottle.get("/prijava")
def prijava_get():
    return bottle.template("prijava.html")

@bottle.post("/prijava")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("prijava.html")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo)
        bottle.response.set_cookie(ime_piskotka, uporabnisko_ime, skrivnost, path="/")
        bottle.redirect("/glavna-stran")
    except ValueError:
        return bottle.template("prijava.html")
    
@bottle.get("/registracija")
def registracija_get():
    return bottle.template("registracija")

@bottle.post("/registracija")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo)
        bottle.response.set_cookie(ime_piskotka, uporabnisko_ime, secret=skrivnost, path="/")
        bottle.redirect("/prijava")
    except ValueError:
        return bottle.template("registracija.html")

@bottle.post("/odjava")
def odjava():
    bottle.response.delete_cookie(ime_piskotka)
    bottle.redirect("/prijava")



bottle.run(debug=True, reloader=True)