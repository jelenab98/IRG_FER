import numpy as np
"""
Odlučila sam koristiti već implementirane funkcije iz biblioteke numpy
np.add - zbrajanje dva vektora
np.vdot - skalarni produkt
np.cross - vektorski produkt
np.linalg.norm - norma 2 za vektor, korijen od zbroja kvadrata koeficijenata
-1*v - suprotni vektor, samo zamjena orijentacije
zbrajanje matrica- samo mat1+mat2
množenje matrica- np.matmul, da stavimo * množili bi se skalarski kao
trasponiranje matrice - transpose()
inverz matrice - np.linalg.inv(matrica, argumenti), ako je bez onda je normalno samo

"""
if __name__ == "__main__":
    v1 = np.add(np.array([2, 3, -4]), np.array([-1, 4, -1]))
    s = np.vdot(v1, np.array([-1, 4, -1]))
    v2 = np.cross(v1, np.array([2, 2, 4]))
    v3 = v2/np.linalg.norm(v2)
    v4 = -1*v2
    M1 = np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]]) + np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])
    M2 = np.matmul(np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]]),
                   np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]]).transpose())
    M3 = np.matmul(np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]]),
                   np.linalg.inv(np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])))

    print('V1 =', v1)
    print('S =', s)
    print('V2 =', v2)
    print('V3 =', v3)
    print('V4 =', v4)
    print('M1 =\n', M1)
    print('M2 =\n', M2)
    print('M3 =\n', M3)
