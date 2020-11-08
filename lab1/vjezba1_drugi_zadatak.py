import numpy as np

if __name__ == '__main__':
    l1 = list(float(i) for i in input('Upisite parametre prvog sustava odvojene zarezom >> ').split(','))
    l2 = list(float(i) for i in input('Upisite parametre drugog sustava odvojene zarezom >> ').split(','))
    l3 = list(float(i) for i in input('Upisite parametre trećeg sustava odvojene zarezom >> ').split(','))

    A = np.array([l1[0:-1], l2[0:-1], l3[0:-1]])
    B = np.array([l1[-1], l2[-1], l3[-1]])

    if np.linalg.det(A) != 0:
        result = np.linalg.solve(A, B)      # koristimo gotovu funkciju u sklopu biblioteke numpy za računanje rješenja
        print("Za A =\n {}\ni B =\n {},\nx =\n {}".format(A, B, result))
    else:
        print("Matrica je singularna! Upiši valjane podatke sljedeći put!")