import bottle


@bottle.get("/")
def osnovna_stran():
    return bottle.template("osnovna_stran.html")

@bottle.get("/prijava")
def prijava_get():
    return bottle.template("prijava.html")

@bottle.post("/prijava")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    
@bottle.get("/registracija")
def registracija_get():
    return bottle.template("registracija")

@bottle.post("/registracija")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")

    
bottle.run(debug=True, reloader=True)