from pyglet.gl import *
from pyglet import clock
from pyglet.window import key, mouse
import math
import numpy as np

window = pyglet.window.Window(800, 600)
triCol = [0.0, 0.0, 0.0]
normalan_bezier = False
t = 0.0
t_pomak = 1
prva = True

@window.event
def on_draw():
    global normalan_bezier
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(2*tijelo.x_min - tijelo.x_max, 2*tijelo.x_max - tijelo.x_min,
               2*tijelo.y_min - tijelo.y_max, 2*tijelo.y_max - tijelo.y_min)
    glMatrixMode(gl.GL_MODELVIEW)

    glLoadIdentity()
    glClearColor(0.5, 0.3, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # iscrtavanje kontrolnih točaka
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for x, y, z in tijelo.kontrola.values():
        glColor3f(0.7, 0.7, 0.7)
        glVertex3f(x, y, z)
    glEnd()

    # iscrtavanje kontrolnog poligona
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for i in range(0, len(tijelo.kontrola)-1):
        x1, y1, z1 = tijelo.kontrola.get(i)
        x2, y2, z2 = tijelo.kontrola.get(i+1)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
    glEnd()

    # bezierova krivulja za kontrolne točke
    tt = 0.0
    n = len(tijelo.kontrola) - 1
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    while tt <= 1.0:
        x, y, z = 0, 0, 0
        i = 0
        for x_k, y_k, z_k in tijelo.kontrola.values():
            b = (math.factorial(n)/(math.factorial(i)*math.factorial(n-i))) * pow(tt, i) * pow(1-tt, n-i)
            x += b*x_k
            y += b*y_k
            z += b*z_k
            i += 1
        glVertex3f(x, y, z)
        tt += 0.01
    glEnd()
    if not normalan_bezier:
        animiraj_beziera(1)


def animiraj_beziera(dt):
    global normalan_bezier, t, t_pomak, prva

    if not normalan_bezier:
        t += t_pomak
        if t <= 0.0:
            t_pomak = 1.0
        elif t >= 100.0:
            t_pomak = -1.0
        t_t = t/100
        x, y, z = 0, 0, 0
        i = 0
        n = len(tijelo.kontrola) - 1
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(8.0)
        glBegin(GL_POINTS)
        for x_k, y_k, z_k in tijelo.kontrola.values():
            b = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * pow(t_t, i) * pow(1 - t_t, n - i)
            x += b * x_k
            y += b * y_k
            z += b * z_k
            i += 1
        glVertex3f(x, y, z)
        glEnd()
        srediste = x, y, z, 1.0
        tijelo.animiranje(srediste)
        glPointSize(2.0)
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        for ravnina in tijelo.ravnine.keys():
            a, b, c, d = tijelo.ravnine.get(ravnina)
            kut = a*tijelo.tocka_O[0] + b*tijelo.tocka_O[1] + c*tijelo.tocka_O[2] + d
            if kut < 0:
                continue
            t1, t2, t3 = tijelo.bridovi.get(ravnina)
            x1, y1, z1, h1 = tijelo.vrhovi_t.get(t1)
            x2, y2, z2, h2 = tijelo.vrhovi_t.get(t2)
            x3, y3, z3, h3 = tijelo.vrhovi_t.get(t3)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
            glVertex3f(x2, y2, z2)
            glVertex3f(x3, y3, z3)
            glVertex3f(x3, y3, z3)
            glVertex3f(x1, y1, z1)
        glEnd()
    if prva:
        clock.schedule_interval_soft(animiraj_beziera, 1.0/10)
        prva = False
    return


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(2*tijelo.x_min - tijelo.x_max, 2*tijelo.x_max - tijelo.x_min,
               2*tijelo.y_min - tijelo.y_max, 2*tijelo.y_max - tijelo.y_min)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()


@window.event
def on_key_press(symbol, modifiers):
    global normalan_bezier
    if symbol == pyglet.window.key.A:
        normalan_bezier = not normalan_bezier
    glFlush()


class Tijelo:
    """
        Klasa Tijelo implementira sve potrebne podatke vezane uz pojedino tijelo koje testiramo i crtamo.
        ---------------------------------------------------------------------------------------------------------------
        Rječnik vrhovi - podaci o koordinatama vrhova, oblik: [redni broj vrha] -> (x, y, z)
        Rječnik brifovi - podaci o poligonima koji tvore tijelo, oblik: [redni broj poligona] -> (vrh1, vrh2, vrh3)
        Rječnik vrhovi_t - podaci o transformiranim koordinatama vrhova koje će se crtati
        Zapis pomak - podaci o pomaku u odnosu na (0, 0, 0) za x, y, z koordinatu
        Zapis tocka_O - podaci o tocki ocista, bilježe se x, y, z koordinata
        Zapis tocka_G - podaci o tocki gledista, bilježe se x, y, z koordinata
        Ime - ime tijela, ukoliko nije definirano u datoteci, uzima se ime datoteke koja se čita
        Rubne vrijednosti kooridnata - koristimo ih za izračun normalizacije tijela na [-1, 1] i računanje središta
        tijela te za centriranje slike u prozoru
        Matrice t - pomoćne matrice koje simuliraju transformaciju nad točkama tijela

        """
    def __init__(self, input_file, koor):
        self.vrhovi = dict()
        self.bridovi = dict()
        self.ravnine = dict()
        self.vrhovi_t = dict()
        self.kontrola = dict()
        self.normale_vrhova = dict()
        self.normirani_vrhovi = dict()
        self.t = np.zeros((4, 4))
        self.t1 = np.zeros((4, 4))
        self.t2 = np.zeros((4, 4))
        self.t3 = np.zeros((4, 4))
        self.t4 = np.array(([0, -1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]))
        self.t5 = np.array(([-1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]))
        self.perspektiva = np.zeros((4, 4))
        self.tocka_O = (1, 1, 3, 1)
        self.tocka_G0 = (0, 0, 0, 1)
        self.srediste = (0, 0, 0, 1)
        self.pomak = (0, 0, 0)
        self.broj_vrhova = 0
        self.broj_bridova = 0
        self.ime = ''
        self.citanje_podataka(input_file, koor)
        self.izracunaj_rubne_koordinate()
        self.izracunaj_srediste_tijela()
        self.izracunaj_pomak()
        self.normalizacija()
        self.odredi_koeficijente()
        self.izracun_matrica()
        self.transformiraj()

    def animiranje(self, srediste):
        x, y, z, h = srediste
        x0, y0, z0, h0 = self.srediste_t
        self.srediste_t = srediste
        matrica_translacije = np.array(([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [x-x0, y-y0, z-z0, 1]))
        for tocka in self.vrhovi_t.keys():
            x, y, z, h = self.vrhovi_t.get(tocka)
            vektor_tocke = np.array([x, y, z, h])
            nova_tocka = np.matmul(vektor_tocke, matrica_translacije)
            x = nova_tocka[0]
            y = nova_tocka[1]
            z = nova_tocka[2]
            z = nova_tocka[3]
            self.vrhovi_t[tocka] = (x, y, z, h)

    def citanje_podataka(self, input_file, file_za_kontrolu):
        """
        Metoda za citanje podataka iz ulazne datoteke.
        Zanemaruju se redovi s početnim znakom # ili nekim drugim znakom.
        Ako redak započinje znakom g, čitamo ime tijela.
        Ako redak započinje znakom v, čitamo vrh tijela i spremamo njegove koordinate.
        Ako redak započinje znakom f, čitamo opis poligona tijela i spremamo vrhove od kojih se sastoji.
        U metodi se također upisuju i koordinate ispitne točke V.
        :param file_za_kontrolu:
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
                self.vrhovi[broj_t + 1] = (float(element[1]), float(element[2]), float(element[3]), 1.0)
                self.normale_vrhova[broj_t + 1] = (0, 0, 0, 0)
            elif line.startswith('f'):
                broj_b = len(self.bridovi.keys())
                element = line.split(' ')
                self.bridovi[broj_b+1] = (int(element[1]), int(element[2]), int(element[3]))
            else:
                continue  # nesto krivo upisano sto ignoriramo

        with open(file_za_kontrolu, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elementi = line.strip('\n').split(' ')
            self.kontrola[len(self.kontrola)] = (float(elementi[0]), float(elementi[1]), float(elementi[2]))

        self.broj_vrhova = len(self.vrhovi.keys())
        self.broj_bridova = len(self.bridovi.keys())
        element_t = input('Upišite x, y, z koordinatu točke O odvojene zarezima >> ').split(',')
        self.tocka_O = (float(element_t[0]), float(element_t[1]), float(element_t[2]), 1.0)
        element_t = input('Upišite x, y, z koordinatu točke G odvojene zarezima >> ').split(',')
        self.tocka_G0 = (float(element_t[0]), float(element_t[1]), float(element_t[2]), 1.0)
        print("Ime: {}| Vrhovi: {}| Bridovi: {}".format(self.ime, self.broj_vrhova, self.broj_bridova))
        print("Tocka O: {}| Tocka G:{}".format(self.tocka_O, self.tocka_G0))
        return

    def izracunaj_rubne_koordinate(self):
        """
        Metoda koja računa rubne koordinate za učitano tijelo.
        :return:
        """
        self.x_min = math.inf
        self.y_min = math.inf
        self.z_min = math.inf
        self.x_max = -math.inf
        self.y_max = -math.inf
        self.z_max = -math.inf
        for x, y, z, h in self.vrhovi.values():
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
                :return:
                """
        x = (self.x_max + self.x_min) / 2
        y = (self.y_max + self.y_min) / 2
        z = (self.z_max + self.z_min) / 2
        self.srediste = (x, y, z, 1.0)
        return

    def izracunaj_pomak(self):
        """
        Metoda za računanje pomaka.
        Budući da je u zadatku definirano da moramo smjestiti tijelo u ishodište, dakle (0, 0, 0), pomak je
        zapravo definiran kao suprotna vrijednost sredista tijela.
        :return:
        """
        dx, dy, dz, h = self.srediste
        self.pomak = (-1*dx, -1*dy, -1*dz, h)
        return

    def normalizacija(self):
        """
        Metoda koja implementira translaciju tijela za neki definirani pomak.
        Pomak se odvija zasebno po x, y i z koordinati.
        Nakon translacije, poziva se izračun rubnih koordinata budući da je došlo do promjene položaja.
        :return:
        """

        dx, dy, dz, h = self.pomak
        m = max(self.x_max - self.x_min, self.y_max - self.y_min, self.z_max - self.z_min)
        factor = 2.0 / m
        matrica_translacije = np.array(([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]))
        matrica_skaliranja = np.array(([factor, 0, 0, 0], [0, factor, 0, 0], [0, 0, factor, 0], [0, 0, 0, 1]))
        matrica_normalizacije = np.matmul(matrica_translacije, matrica_skaliranja)
        for tocka in self.vrhovi.keys():
            x, y, z, h = self.vrhovi.get(tocka)
            vektor_tocke = np.array([x, y, z, h])
            nova_tocka = np.matmul(vektor_tocke, matrica_normalizacije)
            x = nova_tocka[0]
            y = nova_tocka[1]
            z = nova_tocka[2]
            h = nova_tocka[3]
            self.vrhovi[tocka] = (x, y, z, h)
        self.izracunaj_rubne_koordinate()

    def odredi_koeficijente(self):
        """
         Metoda koja računa koefcijente svake ravnine/poligona.
         Koeficijenti se izračunavaju po formuli definiranoj u uputi vježbe.
         :return:
         """
        for ravnina in self.bridovi.keys():
            t1, t2, t3 = self.bridovi.get(ravnina)
            x1, y1, z1, h1 = self.vrhovi.get(t1)
            x2, y2, z2, h2 = self.vrhovi.get(t2)
            x3, y3, z3, h3 = self.vrhovi.get(t3)
            a = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
            b = (z2 - z1)*(x3 - x1) - (x2 - x1)*(z3 - z1)
            c = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
            d = -(a*x1 + b*y1 + c*z1)
            self.ravnine[ravnina] = (a, b, c, d)
        return

    def izracun_matrica(self):
        """
        Metoda koja stvara sve potrebne matrice i finalnu matricu transformacije.
        :return:
        """
        x, y, z, h = self.tocka_O
        x_g, y_g, z_g, h_g = self.tocka_G0
        x1, y1, z1, h1 = x_g - x, y_g - y, z_g - z, h
        self.t1 = np.array(([1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [-x, -y, -z, 1]))

        if x == 0.0 and y == 0.0:
            self.t2[0, 0] = 1
            self.t2[1, 1] = 1
            self.t2[2, 2] = 1
            self.t2[3, 3] = 1
            x2, y2, z2, h2 = x1, y1, z1, h1
        else:
            cos1 = x1 / (math.sqrt(pow(x1, 2) + pow(y1, 2)))
            sin1 = y1 / (math.sqrt(pow(x1, 2) + pow(y1, 2)))
            x2, y2, z2, h2 = math.sqrt(pow(x1, 2) + pow(y1, 2)), 0, z1, h1
            self.t2 = np.array(([cos1, -sin1, 0, 0],
                                [sin1, cos1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]))

        cos2 = z2 / (math.sqrt(pow(x2, 2) + pow(z2, 2)))
        sin2 = x2 / (math.sqrt(pow(x2, 2) + pow(z2, 2)))
        x3, y3, z3, h3 = 0, 0, math.sqrt(pow(x2, 2) + pow(z2, 2)), h2
        self.t3 = np.array(([cos2, 0, sin2, 0],
                            [0, 1, 0, 0],
                            [-sin2, 0, cos2, 0],
                            [0, 0, 0, 1]))

        self.z3 = z3
        self.perspektiva = np.array(([1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 1/self.z3],
                                     [0, 0, 0, 0]))

        self.t = np.matmul(self.t1, self.t2)
        self.t = np.matmul(self.t, self.t3)
        self.t = np.matmul(self.t, self.t4)
        self.t = np.matmul(self.t, self.t5)
        # print(self.t)
        # print(self.perspektiva)
        return

    def transformiraj(self):
        """
        Metoda koja implementira transformaciju  i pomak u perspektivi za sve točke.
        To je definirano kao umnožak matrice i točke.
        :return:
        """
        for index, (x, y, z, h) in enumerate(self.vrhovi.values()):
            vrh = np.array([x, y, z, h])
            t_transform = np.matmul(vrh, self.t)
            t_transform = np.matmul(t_transform, self.perspektiva)
            x = t_transform[0]
            y = t_transform[1]
            z = t_transform[2]
            h = t_transform[3]
            if h != 1 and h != 0:
                x /= h
                y /= h
                z /= h
                h = 1
            self.vrhovi_t[index+1] = (x, y, z, h)
        self.xmin_t = math.inf
        self.xmax_t = -math.inf
        self.ymin_t = math.inf
        self.ymax_t = -math.inf
        for x, y, z, h in self.vrhovi_t.values():
            self.xmin_t = min(self.xmin_t, x)
            self.xmax_t = max(self.xmax_t, x)
            self.ymin_t = min(self.ymin_t, y)
            self.ymax_t = max(self.ymax_t, y)
        self.srediste_t = ((self.xmax_t + self.xmin_t)/2, (self.ymax_t + self.ymin_t)/2, 0, 1)


if __name__ == '__main__':
    datoteke = {1: 'all.obj', 2: 'bird.obj', 3: 'bull.obj', 4: 'dragon.obj', 5: 'frog.obj', 6: 'kocka.obj',
                7: 'porsche.obj', 8: 'skull.obj', 9: 'teapot.obj', 10: 'teddy.obj',
                11: 'temple.obj', 12: 'tetrahedron.obj'}
    print("Ovo je program za prikaz kretanja tijela po Bezierovoj krivulji.")
    print("Upute za korištenje:")
    print("--------------------------------------------------------")
    print("Tipke A - pokretanje ili zaustavljanje kretanja tijela po Bezierovoj krivulji.")
    datoteka = input('Molimo upisite ime datoteke za citanje tocaka >> ')
    print("Mogući odabiri 3D tijela >>", datoteke)
    odabir = int(input('Molimo odaberite jedan broj iz prethodnog izbornika >> '))
    if odabir not in range(1, len(datoteke)+1):
        print('Krivi odabir, sljedeći put odaberite točan broj!')
    else:
        tijelo = Tijelo(datoteke.get(odabir), datoteka)
        pyglet.app.run()
