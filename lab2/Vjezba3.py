import math
from pyglet.gl import *
from pyglet.window import mouse

window = pyglet.window.Window()
triCol = [0.0, 0.0, 0.0]
tocke = list()
crtaj = 0


@window.event
def on_mouse_press(x, y, button, modifiers):
    """
    Metoda koja osluškuje promjene miša na zaslonu.
    Ukoliko je kliknuto lijevom tipkom, iscrtat će se točka i provjerit će se položaj za nju.
    Ukoliko je kliknuto desnom tipkom, poligon će se obojati ili će mu se maknuti boja, ovisno o prethodnom stanju.
    :param x: x koordinata klika
    :param y: y koordinata klika
    :param button:
    :param modifiers:
    :return:
    """
    global triCol, crtaj
    if button & mouse.LEFT:
        tocke.append((x, y))
        provjera_polozaja_tocke((x, y))
    if button & mouse.RIGHT:
        if crtaj == 0:
            print("Slijedi bojanje poligona.")
        else:
            print("Mičem boju s poligona :(")
        crtaj = (crtaj+1) % 2


@window.event
def on_draw():
    """
    Metoda koja ostvaruje crtanje na zaslon. Prvo se iscrtava vanjski obrub poligona pomoću GL_LINE_LOOP.
    Ukoliko je kliknuto mišem da se oboji poligon, poligon će se obojati na način da se iscrtaju vodoravne linije.
    Također, ovdje se iscrtavaju i točke koje su ili zadane iz datoteke ili zadane mišem.
    :return:
    """
    glClearColor(0.5, 0.3, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(triCol[0], triCol[1], triCol[2])

    glBegin(GL_LINE_LOOP)
    for vrh in range(len(poligon.vrhovi)):
        x1, y1, h1 = poligon.vrhovi.get(vrh)
        glVertex2f(x1, y1)
    glEnd()

    if crtaj == 1:
        glBegin(GL_LINES)
        for x1, y1, x2, y2 in poligon.crtanje:
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
        glEnd()

    glColor3f(0.5, 0.5, 0.5)
    glPointSize(6)
    if poligon.tocka:
        glBegin(GL_POINTS)
        for t in poligon.tocka.keys():
            x, y, h = poligon.tocka.get(t)
            glVertex2f(x, y)
        glEnd()

    glBegin(GL_POINTS)
    for x, y in tocke:
        glVertex2f(x, y)
    glEnd()


def provjera_polozaja_tocke(tocka):
    """
    Metoda koja provjera polozaj tocke naspram poligona, a tocka je zadana interaktivno na zaslonu.
    :param tocka: tocka koja je dobivena klikanjem na zaslon, sastoji se od x i y koordinate
    :return:
    """
    x, y = tocka
    for brid, koef in poligon.bridovi.items():
        a, b, c = koef
        koef = a*x + b*y + c
        if koef > 0.0:
            print("Točka ({}, {}) se nalazi izvan poligona!".format(x, y))
            return
    print("Točka ({}, {}) se nalazi unutar poligona!".format(x, y))


class Poligon:
    """
    Klasa koja implementira sve podatke vezane za poligon.
    --------------------------------------------------------------------------------------------------------------------
    Rječnik vrhovi - sadrži podatke o vrhovima, oblik: [redni_broj_vrha] -> (x, y)
    Rječnik točka - sadrži podatke o točkama za porvjeru, oblik: [redni_broj_točke] -> (x,y)
    Rječnik bridovi - sadrži koeficijente za pojedini brid, oblik: [redni_broj_brida] -> (a, b, c)
    Rubne koordinate - služe za bojanje poligona
    Lista crtanje - sadrži informacije o točkama za bojanje poligona, oblik: (L, y, D, y)
    """
    def __init__(self, podaci):
        self.vrhovi = dict()
        self.tocka = dict()
        self.bridovi = dict()
        self.x_min = math.inf
        self.x_max = -math.inf
        self.y_min = math.inf
        self.y_max = -math.inf
        self.crtanje = list()
        self.citanje(podaci)
        self.racunanje_rubnih_kooridnata()
        self.racunanje_koeficijenata_bridova()
        if self.tocka:
            self.provjera_polozaja_tocke()
        self.crtanje_poligona()

    def citanje(self, podaci):
        """
        Metoda kojom se čitaju podaci iz datoteke.
        Retci s # ili nečim drugim se ignoriraju.
        Retci s v označavaju vrh
        Retci s t označavaju točku, no ona nije obvezna.
        :param podaci: ulazna datoteka iz koje se čitaju podaci
        :return:
        """
        with open(podaci, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif line.startswith('v'):
                v, x, y = line.split(' ')
                self.vrhovi[len(self.vrhovi.keys())] = (float(x), float(y), 1.0)
            elif line.startswith('t'):
                t, x, y = line.split(' ')
                self.tocka[len(self.tocka.keys())] = (float(x), float(y), 1.0)
            else:
                continue
        self.vrhovi[len(self.vrhovi.keys())] = self.vrhovi.get(0)
        print("Broj vrhova poligona: {}".format(len(self.vrhovi)-1))
        for vrh, t in self.vrhovi.items():
            if vrh != len(self.vrhovi)-1:
                print("Koordinate {}. vrha: {}, {}".format(vrh+1, t[0], t[1]))
        if self.tocka:
            for tocka, t in self.tocka.items():
                print('Koordinate ispitne točke {}: {}, {}'.format(tocka+1, t[0], t[1]))
        print("Kliknite na zaslon kako biste dodali točke za provjeru.")

    def racunanje_koeficijenata_bridova(self):
        """
        Metoda za računanje koeficijenata bridova.
        Bridovi se računaju iterativno po redoslijedu vrhova.
        :return:
        """
        for vrh in range(len(self.vrhovi.keys())-1):
            x1, y1, h1 = self.vrhovi.get(vrh)
            x2, y2, h2 = self.vrhovi.get(vrh+1)
            a = y1 - y2
            b = x2 - x1
            c = x1*y2 - x2*y1
            self.bridovi[vrh] = a, b, c

    def provjera_polozaja_tocke(self):
        """
        Metoda za provjeru polozaja tocke naspram bridova.
        Provjera se izvrsava za svaki brid, a kad se pronade barem jedan za koji je umnozak veci od 0, provjera se
        prekine i ispise se informacije o polozaju.
        :return:
        """
        for t in self.tocka.keys():
            x, y, h = self.tocka.get(t)
            for brid, koef in self.bridovi.items():
                a, b, c = koef
                koef = a*x + b*y + c
                if koef > 0.0:
                    print("Točka {} se nalazi izvan poligona!".format(t+1))
                    return
            print("Točka {} se nalazi unutar poligona!".format(t+1))

    def racunanje_rubnih_kooridnata(self):
        """
        Metoda za računanje ekstrema, odnosno rubnih koordinata.
        Traže se minimalne i maksimalne vrijednosti za sve vrhove.
        :return:
        """
        for x, y, h in self.vrhovi.values():
            self.x_min = min(self.x_min, x)
            self.x_max = max(self.x_max, x)
            self.y_min = min(self.y_min, y)
            self.y_max = max(self.y_max, y)

    def crtanje_poligona(self):
        """
        Metoda za bojanje poligona implementirana po uputi za labos.
        Točke koje označavaju početnu i krajnju točku za iscrtavanje linije se spremaju u listu te se kasnije iscrtavaju
        :return:
        """
        min_y = round(self.y_min)
        max_y = round(self.y_max)
        for y in range(min_y, max_y):
            l_granica = self.x_min
            d_granica = self.x_max
            for i in range(len(self.vrhovi)-1):
                a, b, c = self.bridovi.get(i)
                if a != 0.0:
                    x = (-b*y - c) / a
                    x1, y1, h1 = self.vrhovi.get(i)
                    x2, y2, h2 = self.vrhovi.get(i+1)
                    if y1 < y2 and x > l_granica:
                        l_granica = x
                    if y1 >= y2 and x < d_granica:
                        d_granica = x
            if l_granica < d_granica:
                self.crtanje.append((l_granica, y, d_granica, y))


if __name__ == '__main__':
    """
    Potrebno je upisati ime datoteke iz koje se čitaju datoteke.
    """
    print("Ovo je program za crtanje konveksnog poligona i provjeru položaja točke.")
    print("Vrhovi poligona čitaju se iz datoteke.")
    print("Točke za provjeru moguće je pročitati iz datoteke ili interaktivno dodati klikanjem na zaslon.")
    print('-----------------------------------------------------------------------------------------')
    print("Upute:\nLijevi klik miša - dodavanje točke\nDesni klik miša - promjena boje  poligona")
    print('-----------------------------------------------------------------------------------------')
    input_file = 'proba.txt'
    poligon = Poligon(input_file)
    pyglet.app.run()
