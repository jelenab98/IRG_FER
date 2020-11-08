import numpy as np
"""
Računa rješenje baricentričnog sustava.
Zanemarujemo slučaj da su dvije iste točke poslane.
Razrađujemo slučaj kad je jedna koordinata u ishodištu ili kad je cijeli jedan stupac 0.
Ako je redak nula, taj redak zamijenimo s 1 1 1, te dodamo 1 kao rješenje tog sustava i računamo konačno rješenje.
Ako je stupac nula, brišemo taj stupac i računamo sustav od dvije nepoznanice, a treću dobijemo kao 1-druga-treća.
Input: dvije matrice A (parametri uz nepoznanice) i B (vrijednosti pojedniog sustava)
Output: 1x3 matrica odgovarajućih vrijednosti uz nepoznanice
"""


def barycentric_coordinates(a, b):

    if (~a.any(axis=1)).any():      # tražimo u kojem retku su sve nule
        location = np.where(~a.any(axis=1))[0]
        a[location, :] = 1
        b[location] = [1]

    if (~a.any(axis=0)).any():      # tražimo  u kojem stupcu su sve nule
        location = np.where(~a.any(axis=0))[0]
        c = np.delete(a, location, axis=1)
        c = np.delete(c, 0, axis=0)
        if np.linalg.det(c) == 0:
            raise Exception()
        d = np.delete(b, 0, axis=0)
        e = np.linalg.solve(c, d)
        t0 = 1 - np.sum(e)
        return np.array([t0, e[0], e[1]])

    if np.linalg.det(a) == 0:
        raise Exception

    return np.linalg.solve(a, b)


if __name__ == '__main__':
    l1 = list(float(i) for i in input('Upisite koordinate prvog vrha odvojene zarezom >> ').split(','))
    l2 = list(float(i) for i in input('Upisite koordinate drugog vrha odvojene zarezom >> ').split(','))
    l3 = list(float(i) for i in input('Upisite koordinate trećeg vrha  odvojene zarezom >> ').split(','))
    l4 = list(float(i) for i in input('Upišite koordinate točke T odvojene zarezom >> ').split(','))

    A = np.array([[l1[0], l2[0], l3[0]], [l1[1], l2[1], l3[1]], [l1[2], l2[2], l3[2]]])
    B = np.array([l4[0], l4[1], l4[2]])

    try:
        result = barycentric_coordinates(A, B)
        print("Za A =\n {}\ni T =\n {},\nbaricentrične koordinate su\n {}".format(A, B, result))
    except:
        print("Matrica je singularna, unesi ispravne točke sljedeći put!")
