from tkinter import *
import numpy as np
import random as rd
import math
from math import e,log
import matplotlib.pyplot as plt

# ====================
# Przykładowe funkcje:
# ====================

# Funkcja Rosenbrock'a:
# Kostka: [-2 < x1 < 2] , [-2 < x2 < 2]
# Punkt optymalny: x = [1.0, 1.0]   f(x) = 0.0
# 100*(x2-x1**2)**2+(1-x1)**2

# Funkcja Goldsteina-Price'a z czterema minimami lokalnymi:
# Kostka: [-3 < x1 < 3] , [-3 < x2 < 3]
# Punkt optymalny: Minimum globalne: x = [0.0, -1.0]   f(x) = 3.0
#                  Minima lokalane:  x = [1.2, 0.8]    f(x) = 840.0
#                                    x = [1.8, 0.2]    f(x) = 84.0
#                                    x = [-0.6, -0.4]  f(x) = 30.0
# (1+(x1+x2+1)**2*(19-14*x1+3*x1**2-14*x2+6*x1*x2+3*x2**2))*(30+(2*x1-3*x2)**2*(18-32*x1+12*x1**2+48*x2-36*x1*x2+27*x2**2))

# 0-(2*x1**3+x2**3-6*x1-12*x2)
# (2*x1**3+x2**3-6*x1-12*x2)


# Funkcja z eksponentą:
# Kostka: [-2 < x1 < 2] , [-2 < x2 < 2]
# Punkt optymalny: x = [-(1/np.sqrt(2)), 0.0]   f(x) = -1/np.sqrt(2*np.exp(1)) ~ -0.42888
# x1*np.exp(-(x1**2+x2**2))

# Funkcja z funkcjami trygonometrycznymi i eksponentą:
# Kostka: [-1, 1] , [-1, 1]
# Punkt optymalny: x = [1078.49, -975.748]  f(x) = -1
# np.sin(x1)*np.sin(x2)*np.exp(-(x1**2+x2**2))

# Funkcja Himmelblau'a:
# Kostka: [-6, 6] , [-6, 6]
# (x1**2+x2-11)**2+(x1+x2**2-7)**2-200

# Funkcja Zangwill'a:
# Punkt optymalny: x = [0.0, 0.0, 0.0]  f(x) = 0.0
# (x1-x2+x3)**2+(-x1+x2+x3)**2+(x1+x2-x3)**2


def fn(x1,x2,**x345):
    if x345.get("x3"):
        x3 = x345.get("x3")
    if x345.get("x4"):
        x4 = x345.get("x4")
    if x345.get("x5"):
        x5 = x345.get("x5")
    return eval(wzor)

#def fn(x1,x2,x3):
#    return eval(wzor)

#def fn(x1,x2,x3,x4):
#    return eval(wzor)

#def fn(x1,x2,x3,x4,x5):
#    return eval(wzor)

def przypisz_fn(n):
    zmienne = []
    if(n==2):
        zmienne = ["x1","x2"]
    if(n==3):
        zmienne = ["x1","x2","x3"]
    if(n==4):
        zmienne = ["x1","x2","x3","x4"]
    if(n==5):
        zmienne = ["x1","x2","x3","x4","x5"]
    return zmienne

def tworz(n, x1_min,x1_max,x2_min,x2_max):
    P=[]
    l=[]

    for i in range(n+1):
        for j in range(n):
            l.append(rd.uniform(x1_min,x1_max))
            #l.append(rd.uniform(x2_min,x2_max))
        P.append(l)
        l=[]
    return P

def oblicz(P, n):
    F=[]
    for i in range(n+1):
        if n==2:
            F.append(fn(P[i][0],P[i][1]))
        if n==3:
            F.append(fn(P[i][0],P[i][1],x3 = P[i][2]))
        if n==4:
            F.append(fn(P[i][0],P[i][1],x3 = P[i][2],x4 = P[i][3]))
        if n==5:
            F.append(fn(P[i][0],P[i][1],x3 = P[i][2],x4 = P[i][3],x5 = P[i][4]))
    return F

def min(F,n):
    min = 0
    for i in range(n+1):
        if F[i] < F[min] :
            min = i
    return min

def max(F,n):
    max = 0
    for i in range(n+1):
        if F[i] > F[max] :
            max = i
    return max

def srodek(P, n, h):
    sum = []
    for i in range(n):
        sum.append(0)

    for j in range(n+1):
        if j != h :
            for k in range(n):
                sum[k] += P[j][k]
    for l in range(n):
        sum[l] /= n
    return sum

def odbicie(P,srodek,h,a,n):
    odb = []
    for i in range(n):
        odb.append((1+a)*srodek[i]-a*P[h][i])
    return odb

def ekspansja(srodek,Pt,y,n):
    eks = []
    for i in range(n):
        eks.append((1+y)*Pt[i]-y*srodek[i])
    return eks

def kontrakcja(b,MAX,Pp,P,n):
    kontr = []
    for i in range(n):
        kontr.append(b * P[MAX][i] + (1- b) * Pp[i])
    return kontr

def czy_Fo_najwieksze(F,MAX,Fo,n):
    for i in range(n+1):
        if i != MAX:
            if Fo >= F[i]:
                buff = True
            else:
                buff = False
    return buff

def odleglosci_miedzy_p(P,n):
    Dlugosci = []
    buff = 0
    for i in range(n+1):
        for j in range(n):
            if i!=n:
                buff += (P[i][j] - P[i+1][j]) ** 2
            else:
                buff += (P[i][j] - P[0][j]) ** 2
        Dlugosci.append(math.sqrt(buff))
    return Dlugosci

def redukcja_simplexu(P,l,n):
    Zredukowany_Simplex = []
    Bufor = []

    for j in range(n+1):
        for k in range(n):
            Bufor.append((P[j][k] + P[l][k])/2)
        Zredukowany_Simplex.append(Bufor)
        Bufor = []

    return Zredukowany_Simplex

def liczenie_fn(n,punkt):
    if n==2:
        wart = fn(punkt[0],punkt[1])
    if n==3:
        wart = fn(punkt[0],punkt[1],x3 = punkt[2])
    if n==4:
        wart = fn(punkt[0],punkt[1],x3 = punkt[2],x4 = punkt[3])
    if n==5:
        wart = fn(punkt[0],punkt[1],x3 = punkt[2],x4 = punkt[3],x5 = punkt[4])
    return wart

def ile_zmiennych(wzor):
    buff = []
    for i in range(len(wzor)):
        if wzor[i] == 'x':
            if wzor[i+1] == '1':
                buff.append(wzor[i+1])
            if wzor[i+1] == '2':
                buff.append(wzor[i+1])
            if wzor[i+1] == '3':
                buff.append(wzor[i+1])
            if wzor[i+1] == '4':
                buff.append(wzor[i+1])
            if wzor[i+1] == '5':
                buff.append(wzor[i+1])
    #print(buff)
    liczba_zmiennych = buff[0]
    for i in range(len(buff)):
        if liczba_zmiennych < buff[i]:
            liczba_zmiennych = buff[i]
    #print(liczba_zmiennych)
    return liczba_zmiennych


#wzor = "(x1 - x2 + x3)**2 + (x2 + x3 - x1)**2 + (x1 + x2 - x3)**2"
#wzor = "100*(x2 - x1**2)**2 + (1-x1)**2"
#wzor = "(x1-2)**2 + (x2-2)**2"
wzor="x1*np.exp(-(x1**2+x2**2))"
#wzor="np.sin(x1+x2)+(x1-x2)**2-1.5*x1+2.5*x2+1"
#wzor="(x1**2-np.cos(18*x1))+(x2**2-np.cos(18*x2))+(x3**2-np.cos(18*x3))"
#(1+(x1+x2+1)**2*(19-14*x1+3*x1**2-14*x2+6*x1*x2+3*x2**2))*(30+(2*x1-3*x2)**2*(18-32*x1+12*x1**2+48*x2-36*x1*x2+27*x2**2))

epsilon = 1*10** (-3)   #dokladnosc obliczen
iteracje = 200         #ograniczenie do 200 powtorzen petli
x1_min = -1             #wymiary kostki
x1_max = 1
x2_min = -1
x2_max = 1

x0 = 0      #p-t startowy
d = 0       #poczatkowa odleglosc miedzy wierzcholkami simpleksu
a = 1       #wspolczynnik odbicia (a>0)
b = 0.5     #wspolczynnik kontrakcji (0<b<1)
y = 1       #wspolczynnik ekspansji (y>0)
n = int(ile_zmiennych(wzor))       #liczba zmiennych niezależnych
#print(n)
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
#fn = eval(wzor)   #stworzenie funkcji dla wzoru

#tablice do przekazywania informacji dla aplikacji
tablica_wynikow = []
tablica_simpleksu = []
global liczba_iter
pkt1 = []
pkt2 = []
pkt3 = []

def algorytm(epsilon, n, a, b, y, iteracje,x1_min,x1_max,x2_min,x2_max):
    global liczba_iter
    liczba_iter = 0
    # tworzenie simpleksu
    P = tworz(n,x1_min,x1_max,x2_min,x2_max)
    odleglosci = odleglosci_miedzy_p(P,n)
    if odleglosci[max(odleglosci,n)] > epsilon:
        stop = True
    else:
        stop = False

    #print(P)
    while stop:
        # liczenie wartosci f-cji w punktach wierzcholkowych simpleksu
        F = oblicz(P,n)
        #print(F)

        # wyznaczenie p-tow z najwieksza i najmniejsza wartoscia funkcji
        MIN = min(F,n)
        MAX = max(F,n)

        # obliczenie środka symetrii simpleksu
        Pp = srodek(P,n,MAX)
        #print(Pp)

        # wyliczenie wartości f-cji dla srodka symetrii simpleksu
        #print(fn(Pp[0],Pp[1]))
        if n==2:
            tablica_wynikow.append([Pp[0], Pp[1], fn(Pp[0],Pp[1]), odleglosci[max(odleglosci,n)]])
        if n==3:
            tablica_wynikow.append([Pp[0], Pp[1], Pp[2], fn(Pp[0],Pp[1],x3 = Pp[2]), odleglosci[max(odleglosci,n)]])
        if n==4:
            tablica_wynikow.append([Pp[0], Pp[1], Pp[2], Pp[3], fn(Pp[0],Pp[1],x3 = Pp[2],x4 = Pp[3]), odleglosci[max(odleglosci,n)]])
        if n==5:
            tablica_wynikow.append([Pp[0], Pp[1], Pp[2], Pp[3], Pp[4], fn(Pp[0],Pp[1],x3 = Pp[2],x4 = Pp[3],x5 = Pp[4]), odleglosci[max(odleglosci,n)]])
        tablica_simpleksu.append(P)

        if n == 2:
            pkt1.append([P[0][0],P[1][0],P[2][0],P[0][0]])
            pkt2.append([P[0][1],P[1][1],P[2][1],P[0][1]])
            pkt3.append([fn(P[0][0],P[0][1]),fn(P[1][0],P[1][1]),fn(P[2][0],P[2][1]),fn(P[0][0],P[0][1])])
        #print(P)

        # odbicie p-tu max wzgledem srodka symetrii simpleksu
        Pt = odbicie(P,Pp,MAX,a,n)
        Fo = liczenie_fn(n,Pt)
        #print(Pt)

        # sprawdzenie czy wartosc f-cji w odbitym p-cie jest wieksza od min
        if liczenie_fn(n,Pt) < liczenie_fn(n,P[MIN]):
            Ptt = ekspansja(Pp,Pt,y,n)
            Fe = liczenie_fn(n,Ptt)
            if Fe < liczenie_fn(n,P[MIN]):
                P[MAX] = Ptt
            else:
                P[MAX] = Pt
            odleglosci = odleglosci_miedzy_p(P,n)
            if odleglosci[max(odleglosci,n)] < epsilon:
                stop = False

        if liczenie_fn(n,Pt) > liczenie_fn(n,P[MIN]):
            if czy_Fo_najwieksze(F,MAX,Fo,n):
                if Fo < F[MAX]:
                    P[MAX] = Pt
            Pttt = kontrakcja(b,MAX,Pp,P,n)
            Fk = liczenie_fn(n,Pttt)
            if Fk >= liczenie_fn(n,P[MAX]):
                P = redukcja_simplexu(P,MIN,n)
            else:
                P[MAX] = Pttt
            if czy_Fo_najwieksze(F, MAX, Fo,n) == False:
                P[MAX] = Pt
            odleglosci = odleglosci_miedzy_p(P,n)
            if odleglosci[max(odleglosci,n)] < epsilon:
                stop = False

        if liczenie_fn(n,Pt) == liczenie_fn(n,P[MIN]):
            print("Blad obliczen")

        liczba_iter += 1
        if liczba_iter == iteracje:
            stop = False

    #print(Pp)
    #print(liczenie_fn(n,Pp))
    #print(liczba_iter)
    #print(dupa)
    #print("Koniec dzialania programu")
    #print(tablica_simpleksu)
    return Pp, liczenie_fn(n,Pp), liczba_iter

#funkcja do wywoływania algorytmu w oknie aplikacji
def start():
    return algorytm(epsilon, int(ile_zmiennych(wzor)), a, b, y, iteracje,x1_min,x1_max,x2_min,x2_max)