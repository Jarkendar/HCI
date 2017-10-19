import numpy as np
import sympy as sym
from matplotlib import pyplot as plt


def sympyTask1():
    print("\nSympy zadanie 1: ")
    x = sym.symbols("x")
    eq = (-x ** 3 + 3 * x ** 2 + 10 * x - 24)
    roz = []
    war = np.arange(-5, 5.1, 0.1)
    for i in war:
        roz.append(eq.evalf(subs={x: i}))
    x0 = sym.solve(eq, x)
    plt.figure(1)
    plt.plot(war, roz)
    plt.plot(x0, [0, 0, 0], 'o')
    plt.savefig("sympyTask1.pdf")
    print("PDF wygenerowany.")


def sympyTask2_3():
    print("\nSympy zadanie 2 i 3: ")
    x, y = sym.symbols("x y")
    eq1 = (x ** 2 + 3 * y - 10)
    eq2 = (4 * x - y ** 2 + 2)
    print("Równanie 1 : ", eq1)
    print("Równanie 2 : ", eq2)
    eq = sym.solve([eq1, eq2], {x, y})
    print("Rozwiązania: ", eq)
    print("Liczba rozwiązań: ", len(eq))


def sympyTask4():
    print("\nSympy zadanie 4: ")
    x, y = sym.symbols("x y")
    eq1 = (x ** 2 + 3 * y - 10)
    eq2 = (4 * x - y ** 2 + 2)
    print("Równanie 1 : ", eq1)
    print("Równanie 2 : ", eq2)
    eq = sym.solve([eq1, eq2], {x, y})
    for s in eq:
        for k, v in s.items():
            print(k, v.evalf())


def sympyTask5():
    print("\nSympy zadanie 5: ")
    x = sym.symbols("x")
    eq = (sym.sin(sym.log(x, 2)) * (sym.cos(x ** 2) / x))
    print("Równanie : ", eq)
    deq = eq.diff()
    print("Pochodna : ", deq)


def numpyTask1():
    print("\nNumpy zadanie 1: ")
    M = np.array([[1, 3, 1, 2], [1, 2, 5, 8], [3, 1, 2, 9], [5, 4, 2, 1]])
    print(M)
    return M


def numpyTask2(M):
    print("\nNumpy zadanie 2: ")
    N = M[1:3, 0:3]
    print(N)
    return N


def numpyTask3():
    print("\nNumpy zadanie 3: ")
    M = np.array([[2, 3, 1], [5, 1, 3]])
    print(M)
    return M


def numpyTask4(M):
    print("\nNumpy zadanie 4: ")
    N = M.T
    print(N)
    return N


def numpyTask5(M, N):
    print("\nNumpy zadanie 5: ")
    L = M.dot(N)
    print(L)


def numpyTask6():
    print("\nNumpy zadanie 6: ")
    xpi = np.arange(-np.pi, np.pi + 1, np.pi)
    xpi5 = np.arange(-np.pi, np.pi + 0.001, 2 * np.pi / 10)
    xpi50 = np.arange(-np.pi, np.pi + 0.001, 2 * np.pi / 100)
    plt.figure(2)
    plt.plot(xpi, np.sin(xpi))
    plt.plot(xpi5, np.sin(xpi5))
    plt.plot(xpi50, np.sin(xpi50))
    plt.savefig("numpyTask6.pdf")
    print("PDF wygenerowany.")


def main():
    sympyTask1()
    sympyTask2_3()
    sympyTask4()
    sympyTask5()

    M = numpyTask1()
    M = numpyTask2(M)
    N = numpyTask3()
    N = numpyTask4(N)
    numpyTask5(M, N)
    numpyTask6()


if __name__ == '__main__':
    main()
