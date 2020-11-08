from pyglet.gl import *
from pyglet.window import key, mouse
import math
import numpy as np

window = pyglet.window.Window(800, 600)
triCol = [0.0, 0.0, 0.0]
pomak = 0.5
crtaj_prednje = True
sjencaj_prvi = False
sjencaj_drugi = False


@window.event
def on_draw():
    global crtaj_prednje, sjencaj_prvi, sjencaj_drugi

    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(tijelo.x_min - (tijelo.x_max - tijelo.x_min) / 2, tijelo.x_max + (tijelo.x_max - tijelo.x_min) / 2,
               tijelo.y_min - (tijelo.y_max - tijelo.y_min) / 2, tijelo.y_max + (tijelo.y_max - tijelo.y_min) / 2)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(5.0)
    glColor3f(0, 1.0, 0)
    if crtaj_prednje:
        x, y, z, h = tijelo.tocka_O
        glBegin(GL_LINES)
        for ravnina in tijelo.prednji:
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
    if sjencaj_prvi:
        x, y, z, h = tijelo.izvor
        xo, yo, zo, ho = tijelo.tocka_O
        amb = tijelo.ia * tijelo.ka
        tijelo.boje_ravnine = list()
        glBegin(GL_TRIANGLES)
        for index, (a, b, c, d) in tijelo.ravnine.items():
            if (xo*a + yo*b + zo*c + d) > 0:
                norma = math.sqrt(pow(a, 2) + pow(b, 2) + pow(c, 2))
                a /= norma
                b /= norma
                c /= norma

                t1, t2, t3 = tijelo.bridovi.get(index)
                x1, y1, z1, h1 = tijelo.vrhovi_t.get(t1)
                x2, y2, z2, h2 = tijelo.vrhovi_t.get(t2)
                x3, y3, z3, h3 = tijelo.vrhovi_t.get(t3)

                x0 = (x1 + x2 + x3) / 3
                y0 = (y1 + y2 + y3) / 3
                z0 = (z1 + z2 + z3) / 3
                x0 = x - x0
                y0 = y - y0
                z0 = z - z0
                norma = math.sqrt(pow(x0, 2) + pow(y0, 2) + pow(z0, 2))
                x0 /= norma
                y0 /= norma
                z0 /= norma

                ln = a * x0 + b * y0 + c * z0
                dif = tijelo.ii * tijelo.kd * ln
                if dif < 0:
                    dif = 0
                i = amb + dif
                i /= 255.0

                glColor3f(0.0, i, 0.0)
                glVertex3f(x1, y1, z1)
                glVertex3f(x2, y2, z2)
                glVertex3f(x3, y3, z3)
        glEnd()
    if sjencaj_drugi:
        glBegin(GL_TRIANGLES)
        x, y, z, h = tijelo.izvor
        xo, yo, zo, ho = tijelo.tocka_O
        amb = tijelo.ia * tijelo.ka
        dif = tijelo.ii * tijelo.kd
        for index, (t1, t2, t3) in tijelo.bridovi.items():
            a, b, c, d = tijelo.ravnine.get(index)
            if (a*xo + b*yo + c*zo + d) > 0:
                x1, y1, z1, h = tijelo.vrhovi_t.get(t1)
                x2, y2, z2, h = tijelo.vrhovi_t.get(t2)
                x3, y3, z3, h = tijelo.vrhovi_t.get(t3)

                n1, n1_x, n1_y, n1_z = tijelo.normale_vrhova.get(t1)
                n2, n2_x, n2_y, n2_z = tijelo.normale_vrhova.get(t2)
                n3, n3_x, n3_y, n3_z = tijelo.normale_vrhova.get(t3)

                norma1 = math.sqrt(pow(n1_x, 2) + pow(n1_y, 2) + pow(n1_z, 2))
                norma2 = math.sqrt(pow(n2_x, 2) + pow(n2_y, 2) + pow(n2_z, 2))
                norma3 = math.sqrt(pow(n3_x, 2) + pow(n3_y, 2) + pow(n3_z, 2))

                n1_x /= norma1
                n1_y /= norma1
                n1_z /= norma1

                n2_x /= norma2
                n2_y /= norma2
                n2_z /= norma2

                n3_x /= norma3
                n3_y /= norma3
                n3_z /= norma3

                x1n, y1n, z1n = x-x1, y-y1, z-z1
                x2n, y2n, z2n = x-x2, y-y2, z-z2
                x3n, y3n, z3n = x-x3, y-y3, z-z3

                norma1 = math.sqrt(pow(x1n, 2) + pow(y1n, 2) + pow(z1n, 2))
                norma2 = math.sqrt(pow(x2n, 2) + pow(y2n, 2) + pow(z2n, 2))
                norma3 = math.sqrt(pow(x3n, 2) + pow(y3n, 2) + pow(z3n, 2))

                x1n /= norma1
                y1n /= norma1
                z1n /= norma1

                x2n /= norma2
                y2n /= norma2
                z2n /= norma2

                x3n /= norma3
                y3n /= norma3
                z3n /= norma3

                ln1 = n1_x*x1n + n1_y*y1n + n1_z*y1n
                ln2 = n2_x*x2n + n2_y*y2n + n2_z*z2n
                ln3 = n3_x*x3n + n3_y*y3n + n3_z*z3n

                dif1 = dif*ln1
                if dif1 < 0:
                    dif1 = 0
                i1 = amb + dif1
                i1 /= 255.0

                dif2 = dif * ln2
                if dif2 < 0:
                    dif2 = 0
                i2 = amb + dif2
                i2 /= 255.0
                dif3 = dif * ln3
                if dif3 < 0:
                    dif3 = 0
                i3 = amb + dif3
                i3 /= 255.0

                glColor3f(0.0, i1, 0.0)
                glVertex3f(x1, y1, z1)
                glColor3f(0.0, i2, 0.0)
                glVertex3f(x2, y2, z2)
                glColor3f(0.0, i3, 0.0)
                glVertex3f(x3, y3, z3)
        glEnd()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(tijelo.x_min - (tijelo.x_max - tijelo.x_min), tijelo.x_max + (tijelo.x_max - tijelo.x_min),
               tijelo.y_min - (tijelo.y_max - tijelo.y_min), tijelo.y_max + (tijelo.y_max - tijelo.y_min))
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()


@window.event
def on_key_press(symbol, modifiers):
    global pomak, crtaj_prednje, sjencaj_prvi, sjencaj_drugi
    if symbol == pyglet.window.key.Q:
        tijelo.citaj('g_x', pomak)
    elif symbol == pyglet.window.key.W:
        tijelo.citaj('g_y', pomak)
    elif symbol == pyglet.window.key.E:
        tijelo.citaj('g_z', pomak)
    elif symbol == pyglet.window.key.A:
        tijelo.citaj('g_x', -pomak)
    elif symbol == pyglet.window.key.S:
        tijelo.citaj('g_y', -pomak)
    elif symbol == pyglet.window.key.D:
        tijelo.citaj('g_z', -pomak)
    elif symbol == pyglet.window.key.Z:
        tijelo.citaj('o_x', pomak)
    elif symbol == pyglet.window.key.U:
        tijelo.citaj('o_y', pomak)
    elif symbol == pyglet.window.key.I:
        tijelo.citaj('o_z', pomak)
    elif symbol == pyglet.window.key.H:
        tijelo.citaj('o_x', -pomak)
    elif symbol == pyglet.window.key.J:
        tijelo.citaj('o_y', -pomak)
    elif symbol == pyglet.window.key.K:
        tijelo.citaj('o_z', -pomak)
    elif symbol == pyglet.window.key.Y:
        crtaj_prednje = not crtaj_prednje
        sjencaj_prvi = False
        sjencaj_drugi = False
    elif symbol == pyglet.window.key.X:
        sjencaj_prvi = not sjencaj_prvi
        crtaj_prednje = False
        sjencaj_drugi = False
    elif symbol == pyglet.window.key.C:
        sjencaj_drugi = not sjencaj_drugi
        crtaj_prednje = False
        sjencaj_prvi = False
    glFlush()


class Tijelo:
    """
        Klasa Tijelo implementira sve potrebne podatke vezane uz pojedino tijelo koje testiramo i crtamo.
        U ovoj verziji, praćena je uputa za labos i tijelo je prvo translatirano i skalirano pa tek su onda izračunati
        koeficijenti ravnina i provjeren položaj točke naspram tijela. Osobno, ovaj redoslijed mi nema smisla jer
        jedine točke za koje će ova provjera dati rezultat da je točke unutra su one u rasponu [-1, 1].
        Također, u ovoj verziji je srediste tijela izracunato na način da se uzimala aritmetička sredina ekstrema.
        ---------------------------------------------------------------------------------------------------------------
        Rječnik vrhovi - podaci o koordinatama vrhova, oblik: [redni broj vrha] -> (x, y, z)
        Rječnik brifovi - podaci o poligonima koji tvore tijelo, oblik: [redni broj poligona] -> (vrh1, vrh2, vrh3)
        Rječnik ravnine - podaci o koeficijentima pojedine ravnine/poligona,oblik: [redni broj poligona] -> (a, b, c, d)
        Boolean konveksan - označava je li tijelo konveksno kako bismo znali trebamo li ispitivati odnos točke
                          - u zadatku nije navedeno da je potrebno ispitati konveksnost tijela pa navodimo kao ulaz
        Zapis pomak - podaci o pomaku u odnosu na (0, 0, 0) za x, y, z koordinatu
        Zapis tocka_v - podaci o tocki V koju ispitujemo, bilježe se x, y, z koordinata
        Ime - ime tijela, ukoliko nije definirano u datoteci, uzima se ime datoteke koja se čita
        Rubne vrijednosti kooridnata - koristimo ih za izračun normalizacije tijela na [-1, 1] i računanje središta
        tijela
        """
    def __init__(self, input_file):
        self.vrhovi = dict()
        self.bridovi = dict()
        self.ravnine = dict()
        self.ravnine_t = dict()
        self.vrhovi_t = dict()
        self.normale_vrhova = dict()
        self.prednji = list()
        self.boje_ravnine = list()
        self.boje_vrhovi = list()
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
        self.t2_5 = np.zeros((4, 4))
        self.perspektiva = np.zeros((4, 4))
        self.tocka_O = (1, 1, 3, 1)
        self.tocka_G0 = (0, 0, 0, 1)
        self.srediste = (0, 0, 0, 1)
        self.izvor = (0, 0, 0, 1)
        self.pomak = (0, 0, 0)
        self.broj_vrhova = 0
        self.broj_bridova = 0
        self.ime = ''
        self.ii = 200
        self.ia = 50
        self.ka = 0.5
        self.kd = 0.9
        self.citanje_podataka(input_file)
        self.izracunaj_rubne_koordinate()
        self.izracunaj_srediste_tijela()
        self.izracunaj_pomak()
        self.normalizacija()
        self.odredi_koeficijente()
        self.normirane_normale_vrhova()
        self.ukloni_straznje()
        self.izracun_matrica()
        self.transformiraj()

    def citaj(self, opcija, d):
        x, y, z, h = self.tocka_O
        x_g, y_g, z_g, h_g = self.tocka_G0
        if opcija == 'g_x':
            x_g += d
        elif opcija == 'g_y':
            y_g += d
        elif opcija == 'g_z':
            z_g += d
        elif opcija == 'o_x':
            x += d
        elif opcija == 'o_y':
            y += d
        elif opcija == 'o_z':
            z += d

        self.tocka_O = (x, y, z, h)
        self.tocka_G0 = (x_g, y_g, z_g, h_g)
        # print("Tocka O: {}| Tocka G:{}".format(self.tocka_O, self.tocka_G0))
        self.izracun_matrica()
        self.transformiraj()
        self.odredi_koeficijente()
        self.normirane_normale_vrhova()
        self.ukloni_straznje()

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
                self.vrhovi[broj_t + 1] = (float(element[1]), float(element[2]), float(element[3]), 1.0)
                self.normale_vrhova[broj_t + 1] = (0, 0.0, 0.0, 0.0)
            elif line.startswith('f'):
                broj_b = len(self.bridovi.keys())
                element = line.split(' ')
                self.bridovi[broj_b+1] = (int(element[1]), int(element[2]), int(element[3]))
            else:
                continue  # nesto krivo upisano sto ignoriramo

        self.broj_vrhova = len(self.vrhovi.keys())
        self.broj_bridova = len(self.bridovi.keys())
        element_t = input('Upišite x, y, z koordinatu točke O odvojene zarezima >> ').split(',')
        self.tocka_O = (float(element_t[0]), float(element_t[1]), float(element_t[2]), 1.0)
        element_t = input('Upišite x, y, z koordinatu točke G odvojene zarezima >> ').split(',')
        self.tocka_G0 = (float(element_t[0]), float(element_t[1]), float(element_t[2]), 1.0)
        element_t = input('Upišite x, y, z koordinatu točke izvora odvojene zarezima >> ').split(',')
        self.izvor = (float(element_t[0]), float(element_t[1]), float(element_t[2]), 1.0)
        print("Ime: {}| Vrhovi: {}| Bridovi: {}".format(self.ime, self.broj_vrhova, self.broj_bridova))
        print("Tocka O: {}| Tocka G: {}| Izvor: {}".format(self.tocka_O, self.tocka_G0, self.izvor))
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

        if x == 0 and y == 0:
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
                if x == -0.0:
                    x = 0.0
                y /= h
                if y == -0.0:
                    y = 0.0
                z /= h
                if z == -0.0:
                    z = 0.0
                h = 1
            self.vrhovi_t[index+1] = (x, y, z, h)
        self.izracunaj_rubne_koordinate()

    def ukloni_straznje(self):
        x, y, z, h = self.tocka_O
        self.prednji = list()
        for ravnina, (a, b, c, d) in self.ravnine.items():
            kut = a*x + b*y + c*z + d
            if kut > 0:
                self.prednji.append(ravnina)
        return

    def normirane_normale_vrhova(self):
        for t1, t2, t3 in self.bridovi.values():
            self.normale_vrhova[t1] = (0, 0, 0, 0)
            self.normale_vrhova[t2] = (0, 0, 0, 0)
            self.normale_vrhova[t3] = (0, 0, 0, 0)
        for ravnina, (a, b, c, d) in self.ravnine.items():
            t1, t2, t3 = self.bridovi.get(ravnina)

            n, x, y, z = self.normale_vrhova.get(t1)
            n += 1
            x += a
            y += b
            z += c
            self.normale_vrhova[t1] = (n, x, y, z)

            n, x, y, z = self.normale_vrhova.get(t2)
            n += 1
            x += a
            y += b
            z += c
            self.normale_vrhova[t2] = (n, x, y, z)

            n, x, y, z = self.normale_vrhova.get(t3)
            n += 1
            x += a
            y += b
            z += c
            self.normale_vrhova[t3] = (n, x, y, z)
        for vrh, (n, x, y, z) in self.normale_vrhova.items():
            x /= n
            y /= n
            z /= n
            self.normale_vrhova[vrh] = (n, x, y, z)


if __name__ == '__main__':

    datoteke = {1: 'all.obj', 2: 'bird.obj', 3: 'bull.obj', 4: 'dragon.obj', 5: 'frog.obj', 6: 'kocka.obj',
                7: 'porsche.obj', 8: 'skull.obj', 9: 'teapot.obj', 10: 'teddy.obj',
                11: 'temple.obj', 12: 'tetrahedron.obj'}
    print("Ovo je program za prikaz perspektivne projekcije 3D tijela.")
    print("Upute za korištenje:")
    print("--------------------------------------------------------")
    print("Tipke q w e - povećanje očišta za 0.2 za x, y, odnosno z os")
    print("Tipke a s d - smanjenje očišta za 0.2 za x, y, odnosno z os")
    print("Tipke z u i - povećanje gledišta za 0.2 za x, y, odnsno z os")
    print("Tipke h j k - povećanje gledišta za 0.2 za x, y, odnosno z os")
    print("Mogući odabiri 3D tijela >>", datoteke)
    odabir = int(input('Molimo odaberite jedan broj iz prethodnog izbornika >> '))
    if odabir not in range(1, len(datoteke)+1):
        print('Krivi odabir, sljedeći put odaberite točan broj!')
    else:
        tijelo = Tijelo(datoteke.get(odabir))
        pyglet.app.run()
