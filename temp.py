def algorytm(epsilon, n, a, b, y, iteracje,x1_min,x1_max,x2_min,x2_max):
    global liczba_iter
    liczba_iter = 0

    P = tworz(n,x1_min,x1_max,x2_min,x2_max)
    odleglosci = odleglosci_miedzy_p(P,n)
    if odleglosci[max(odleglosci,n)] > epsilon:
        stop = True
    else:
        stop = False

    while stop:
        F = oblicz(P,n)

        MIN = min(F,n)
        MAX = max(F,n)

        Pp = srodek(P,n,MAX)

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

        Pt = odbicie(P,Pp,MAX,a,n)
        Fo = liczenie_fn(n,Pt)

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

    return Pp, liczenie_fn(n,Pp), liczba_iter