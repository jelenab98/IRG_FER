from pyglet.gl import *
import math

window = pyglet.window.Window(800, 600)
triCol = [0.0, 0.0, 0.0]
skalar = 250
pomak = 150
centriranje = 40


@window.event
def on_draw():
    """
     Unutar funkcije draw crtamo tijelo u 2D ravnini (x-y ravnina).
     Ovo je druga verzija programa pa je ovdje navedena i druga verzija iscrtavanja koja iscrtava trokute s ispunom.
     Svi vrhovi su normalizirani na vrijednosti [-1, 1] pa kako bismo vidjeli cijelo tijelo potrebno je provesti
     sljedeće transformacije:
            1. translacija svih koordinata za 2 -- kako bismo se maknuli iz negativnih vrijednosti
            2. uniformno skaliranje skalarom -- kako bi se tijelo povećalo
            3. translacija za pomak i +/- centriranje -- kako bismo tijelo pomaknuli bliže centru prozora
                                                      -- centriranje je provedeno od oka, nije izračunato
     Transformacije su provedeno ručno, a ne matrično jer je jednostavnije.
     """
    glClearColor(0.5, 0.3, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(triCol[0], triCol[1], triCol[2])

    glBegin(GL_TRIANGLES)
    for t1, t2, t3 in tijelo.bridovi.values():
        x1, y1, z1 = tijelo.vrhovi.get(t1)
        x2, y2, z2 = tijelo.vrhovi.get(t2)
        x3, y3, z3 = tijelo.vrhovi.get(t3)
        glVertex3f(skalar * (x1 + 2) - pomak + centriranje, skalar * (y1 + 2) - pomak - centriranje, 0.0)
        glVertex3f(skalar * (x2 + 2) - pomak + centriranje, skalar * (y2 + 2) - pomak - centriranje, 0.0)
        glVertex3f(skalar * (x3 + 2) - pomak + centriranje, skalar * (y3 + 2) - pomak - centriranje, 0.0)
    glEnd()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(gl.GL_MODELVIEW)


class Tijelo:
    """
    Klasa Tijelo implementira sve potrebne podatke vezane uz pojedino tijelo koje testiramo i crtamo.
    U ovoj verziji programa, koeficijenti ravnina tijela računati su prije bilo kakve transformacije jer mi je to
    logičnije od načina iz uputa. Također, središte tijela računato je samo preko rubnih koordinata, a ne svih vrhova.
    -------------------------------------------------------------------------------------------------------------------
    Rječnik vrhovi - podaci o koordinatama vrhova, oblik: [redni broj vrha] -> (x, y, z)
    Rječnik brifovi - podaci o poligonima koji tvore tijelo, oblik: [redni broj poligona] -> (vrh1, vrh2, vrh3)
    Rječnik ravnine - podaci o koeficijentima pojedine ravnine/poligona, oblik: [redni broj poligona] -> (a, b, c, d)
    Boolean konveksan - označava je li tijelo konveksno kako bismo znali trebamo li ispitivati odnos točke
                      - u zadatku nije navedeno da je potrebno ispitati konveksnost tijela pa navodimo kao ulaz
    Zapis pomak - podaci o pomaku u odnosu na (0, 0, 0) za x, y, z koordinatu
    Zapis tocka_v - podaci o tocki V koju ispitujemo, bilježe se x, y, z koordinata
    Ime - ime tijela, ukoliko nije definirano u datoteci, uzima se ime datoteke koja se čita
    Rubne vrijednosti kooridnata - koristimo ih za izračun normalizacije tijela na [-1, 1] i računanje središta tijela
    """
    def __init__(self, input_file, konveksan=False):
        self.vrhovi = dict()
        self.bridovi = dict()
        self.ravnine = dict()
        self.konveksan = konveksan
        self.pomak = 0, 0, 0
        self.tocka_V = 0, 0, 0
        self.ime = input_file[:-4]
        self.x_min = math.inf
        self.y_min = math.inf
        self.z_min = math.inf
        self.x_max = -math.inf
        self.y_max = -math.inf
        self.z_max = -math.inf
        self.citanje_podataka(input_file)
        self.izracunaj_rubne_koordinate()
        self.izracunaj_srediste_tijela()
        self.izracunaj_pomak()
        self.odredi_koeficijente()
        self.translatiraj()
        self.skaliraj()
        if self.konveksan:
            self.provjera_polozaja_tocke()

    def citanje_podataka(self, input_file):
        """
        Metoda za citanje podataka iz ulazne datoteke.
        Zanemaruju se redovi s početnim znakom # ili nekim drugim znakom.
        Ako redak započinje znakom g, čitamo ime tijela.
        Ako redak započinje znakom v, čitamo vrh tijela i spremamo njegove koordinate.
        Ako redak započinje znakom f, čitamo opis poligona tijela i spremamo vrhove od kojih se sastoji.
        U metodi se također upisuju i koordinate ispitne točke V.
        :param input_file:
        :return:
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('#'):
                continue
            elif line.startswith('g'):
                self.ime = line.strip('\n')
            elif line.startswith('v'):
                broj_t = len(self.vrhovi.keys())
                element = line.split(' ')
                self.vrhovi[broj_t + 1] = (float(element[1]), float(element[2]), float(element[3]))
            elif line.startswith('f'):
                broj_b = len(self.bridovi.keys())
                element = line.split(' ')
                self.bridovi[broj_b+1] = (int(element[1]), int(element[2]), int(element[3]))
            else:
                continue  # nesto krivo upisano sto ignoriramo

        self.broj_vrhova = len(self.vrhovi.keys())
        self.broj_bridova = len(self.bridovi.keys())
        print("Ime: {}| Vrhovi: {}| Bridovi: {}".format(self.ime, self.broj_vrhova, self.broj_bridova))
        if self.konveksan:
            element_t = input('Upišite x, y, z koordinatu točke V odvojene zarezima >> ').split(',')
            self.tocka_V = (float(element_t[0]), float(element_t[1]), float(element_t[2]))
        return

    def izracunaj_rubne_koordinate(self):
        """
        Metoda koja računa rubne koordinate za učitano tijelo.
        :return:
        """
        for x, y, z in self.vrhovi.values():
            self.x_max = max(self.x_max, x)
            self.x_min = min(self.x_min, x)
            self.y_max = max(self.y_max, y)
            self.y_min = min(self.y_min, y)
            self.z_max = max(self.z_max, z)
            self.z_min = min(self.z_min, z)
        return

    def izracunaj_srediste_tijela(self):
        """
        Metoda koja računa središte tijela za učitano tijelo.
        Središte tijela je moguće izračunati na dva načina.
        Prvi način je da se se uzme aritmetička sredina svih vrhova tijela.
        Drugi način je da se uzme aritmetička sredina samo rubnih vrijednosti.
        Razlika u izračunu je praktički zanemariva, odnosno razlika je u drugoj ili većoj decimali.
        :return:
        """

        x_suma = 0
        y_suma = 0
        z_suma = 0

        for x, y, z in self.vrhovi.values():
            x_suma += x
            y_suma += y
            z_suma += z

        x_suma /= self.broj_vrhova
        y_suma /= self.broj_vrhova
        z_suma /= self.broj_vrhova

        x = (self.x_max + self.x_min) / 2
        y = (self.y_max + self.y_min) / 2
        z = (self.z_max + self.z_min) / 2
        self.srediste = x, y, z
        return

    def izracunaj_pomak(self):
        """
        Metoda za računanje pomaka.
        Budući da je u zadatku definirano da moramo smjestiti tijelo u ishodište, dakle (0, 0, 0), pomak je zapravo
        definiran kao suprotna vrijednost sredista tijela.
        :return:
        """
        dx = 0.0 - self.srediste[0]
        dy = 0.0 - self.srediste[1]
        dz = 0.0 - self.srediste[2]
        self.pomak = dx, dy, dz

    def translatiraj(self):
        """
        Metoda koja implementira translaciju tijela za neki definirani pomak.
        Pomak se odvija zasebno po x, y i z koordinati.
        Nakon translacije, poziva se izračun rubnih koordinata budući da je došlo do promjene položaja.
        :return:
        """
        dx = self.pomak[0]
        dy = self.pomak[1]
        dz = self.pomak[2]

        for tocka in self.vrhovi.keys():
            x, y, z = self.vrhovi.get(tocka)
            x += dx
            y += dy
            z += dz
            self.vrhovi[tocka] = (x, y, z)
        self.izracunaj_rubne_koordinate()

    def skaliraj(self):
        """
        Metoda koja implementira skaliranje na raspon [-1, 1]. Dakle, zapravo se radi o normalizaciji tijela.
        Normalizacija je provedena u odnosu na najveću vrijednost koordinate (apsolutno gledano).
        Nakon skaliranja, pozvana je metoda za izracun rubnih koordinata budući da je doslo do pomaka tijela.
        :return:
        """
        faktor = max(abs(self.x_min), abs(self.x_max), abs(self.y_min),
                     abs(self.y_max), abs(self.z_min), abs(self.z_max))
        for tocka in self.vrhovi.keys():
            x, y, z = self.vrhovi.get(tocka)
            x *= 1/faktor
            y *= 1/faktor
            z *= 1/faktor
            self.vrhovi[tocka] = (x, y, z)
        self.izracunaj_rubne_koordinate()

    def odredi_koeficijente(self):
        """
        Metoda koja računa koefcijente svake ravnine/poligona.
        Koeficijenti se izračunavaju po formuli definiranoj u uputi vježbe.
        :return:
        """
        for ravnina in self.bridovi.keys():
            t1, t2, t3 = self.bridovi.get(ravnina)
            x1, y1, z1 = self.vrhovi.get(t1)
            x2, y2, z2 = self.vrhovi.get(t2)
            x3, y3, z3 = self.vrhovi.get(t3)
            a = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
            b = (z2 - z1)*(x3 - x1) - (x2 - x1)*(z3 - z1)
            c = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
            d = -(a*x1 + b*y1 + c*z1)
            self.ravnine[ravnina] = (a, b, c, d)
        return

    def provjera_polozaja_tocke(self):
        """
        Metoda koja izračunava položaj točke u odnosu na tijelo.
        Provjerava se umnožak točke i koeficijenata ravnine za svaku ravninu.
        Ukoliko je za barem jednu ravninu umnožak veći od nule, znamo da je točka sigurno izvan tijela.
        :return:
        """
        x, y, z = self.tocka_V
        print("Provjeravam položaj točke V({}, {}, {})".format(x, y, z))
        for a, b, c, d in self.ravnine.values():
            result = a*x + b*y + c*z + d
            if result > 0.0:
                print("Izvan je!")
                return
        print("Unutar je!")


if __name__ == '__main__':
    """
    Potrebno je definirati je li neko tijelo konveksno. Napravila sam kod na ovaj način samo zbog toga što u uputi
    nije navedeno da je potrebno ispitati pojedino tijelo je li konveksno ili ne.
    Moguće datoteke za provjeru:
        -all.obj
        -bird.obj
        -bull.obj
        -dragon.obj
        -frog.obj
        -kocka.obj
        -porsche.obj
        -skull.obj
        -teapot.obj
        -teddy.obj
        -temple.obj
        -tetrahedron.obj
    """
    datoteke = {1: 'all.obj', 2: 'bird.obj', 3: 'bull.obj', 4: 'dragon.obj', 5: 'frog.obj', 6: 'kocka.obj',
                7: 'porsche.obj', 8: 'skull.obj', 9: 'teapot.obj', 10: 'teddy.obj',
                11: 'temple.obj', 12: 'tetrahedron.obj'}
    print("Mogući odabiri 3D tijela >>", datoteke)
    odabir = int(input('Molimo odaberite jedan broj iz prethodnog izbornika >> '))
    if odabir not in range(1, len(datoteke) + 1):
        print('Krivi odabir, sljedeći put odaberite točan broj!')
    else:
        if odabir in (6, 12):
            tijelo = Tijelo(datoteke.get(odabir), True)
        else:
            tijelo = Tijelo(datoteke.get(odabir), False)
        pyglet.app.run()
