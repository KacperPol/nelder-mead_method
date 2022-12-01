from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib import cm

import numpy as np
import sys
import metodaNM as Alg

global iter, krok, X, Y, Z, norm, inf
iter = 0
krok = 0
X = 0
Y = 0
Z = 0
norm = 0

def exit_prog():
    sys.exit(0)

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("algorytm.ui", self)
        self.setWindowTitle("Metoda Pełzającego Simpleksu")

        #self.pushButton_gen.clicked.connect(self.update_graph)

        self.pushButton_uruchom.clicked.connect(self.start_alg)
        self.pushButton_wyjdz.clicked.connect(lambda: exit_prog())
        self.pushButton_rysuj.clicked.connect(self.rysuj_wykres)
        self.pushButton_pop.clicked.connect(self.pop_wykres)
        self.pushButton_nast.clicked.connect(self.nast_wykres)

        # Toolbar - ruchomy
        #self.addToolBar(NavigationToolbar(self.Wykres_widget.canvas, self, coordinates=True))
        
        # Toolbar - w widgetcie
        self.Wykres_widget.vertical_layout.addWidget(NavigationToolbar(self.Wykres_widget.canvas, self, coordinates=True))

    def wczytaj_wszystko(self):
        # print(Alg.epsilon, int(Alg.ile_zmiennych(Alg.wzor)), Alg.a, Alg.b, Alg.y, Alg.iteracje, Alg.x1_min, Alg.x1_max, Alg.x2_min, Alg.x2_max)
        Alg.wzor = str(self.lineEdit_funkcja.text())

        Alg.epsilon = self.doubleSpinBox_epsilon.value()
        Alg.iteracje = int(self.doubleSpinBox_max_iter.value())

        Alg.x1_min = self.doubleSpinBox_x1_min.value()
        Alg.x1_max = self.doubleSpinBox_x1_max.value()
        Alg.x2_min = self.doubleSpinBox_x2_min.value()
        Alg.x2_max = self.doubleSpinBox_x2_max.value()

        Alg.a = self.doubleSpinBox_wsp_odb.value()
        Alg.b = self.doubleSpinBox_wsp_kont.value()
        Alg.y = self.doubleSpinBox_wsp_eks.value()

        Alg.n = int(Alg.ile_zmiennych(Alg.wzor))


    def start_alg(self):
        global krok, iter, inf

        Alg.tablica_wynikow = []
        Alg.tablica_simpleksu = []
        Alg.pkt1 = []
        Alg.pkt2 = []
        Alg.pkt3 = []
        
        self.wczytaj_wszystko()

        #print(str(Alg.start()))
        opt1, opt2, opt3 = Alg.start()
        
        print(opt1, opt2, opt3)
        
        krok = Alg.liczba_iter
        iter += 1
        self.textBrowser_ilosc_krok.clear()
        self.textBrowser_rozw.append("\nWywołanie nr: " + str(iter))
        self.textBrowser_rozw.append("Funkcja: " + str(self.lineEdit_funkcja.text()))
        tekst="Współrzędne wyznaczonego punktu optymalnego: x = [ "
        for i in range(int(Alg.ile_zmiennych(Alg.wzor))+1):
            tekst = tekst + str(Alg.tablica_wynikow[krok - 1][i]) + " "
            if i == int(Alg.ile_zmiennych(Alg.wzor))-1:
                self.textBrowser_rozw.append(tekst + "]")
            elif i > int(Alg.ile_zmiennych(Alg.wzor))-1:
                self.textBrowser_rozw.append("f(x)=" + str(Alg.tablica_wynikow[krok - 1][i]))
        #self.textBrowser_rozw.append("f(x) = "+str(Alg.tablica_wynikow[krok - 1][(int(Alg.ile_zmiennych(Alg.wzor))+1)]))
        self.textBrowser_rozw.append("Największa odległość między dwoma punktami simpleksu: " + str(Alg.tablica_wynikow[krok - 1][int(Alg.ile_zmiennych(Alg.wzor))+1]))
        self.textBrowser_ilosc_krok.append(str(krok))

        self.rysuj_wykres()

        self.textBrowser_temp_krok.clear()


    def rysuj_wykres(self):
        if int(Alg.ile_zmiennych(Alg.wzor)) == 2:
            global X, Y, Z, norm

            self.wczytaj_wszystko()

            jakosc = int(self.doubleSpinBox_jakosc.value())

            x = np.arange(Alg.x1_min, Alg.x1_max, 0.001 * 25)
            y = np.arange(Alg.x2_min, Alg.x2_max, 0.001 * 25)

            #self.Wykres_widget.canvas.axes.clear()
            #self.Wykres_widget.canvas.axes.plot(x, y)
            #self.Wykres_widget.canvas.draw()

            X, Y = np.meshgrid(x, y)
            Z = Alg.fn(X, Y)
            norm = cm.colors.Normalize(vmax=abs(Z).max(), vmin=-abs(Z).max())


            self.Wykres_widget.canvas.axes.clear()
            contourf_ = self.Wykres_widget.canvas.axes.contourf(X, Y, Z, extent=(Alg.x1_min, Alg.x1_max, Alg.x2_min, Alg.x2_max), levels=jakosc, origin='lower', cmap='magma', norm=norm)
            cbar = self.Wykres_widget.canvas.figure.colorbar(contourf_)
            self.Wykres_widget.canvas.axes.plot(Alg.tablica_wynikow[krok - 1][0], Alg.tablica_wynikow[krok - 1][1], 'o', color='white')
            self.Wykres_widget.canvas.axes.plot(Alg.pkt1[krok - 1], Alg.pkt2[krok - 1], '--', color='green')
            self.Wykres_widget.canvas.axes.set_xlim(Alg.x1_min, Alg.x1_max)
            self.Wykres_widget.canvas.axes.set_ylim(Alg.x2_min, Alg.x2_max)
            cbar.remove()
            self.Wykres_widget.canvas.draw()

    def pop_wykres(self):
        global krok
        if Alg.tablica_wynikow != []:
            if krok > 1:
                krok -= 1
                self.textBrowser_temp_krok.clear()
                self.textBrowser_temp_krok.append(str(krok))
                self.nowe_dane()
                self.rysuj_wykres()
                
    def nast_wykres(self):
        global krok
        if Alg.tablica_wynikow != []:
            if krok < Alg.liczba_iter:
                krok += 1
                self.textBrowser_temp_krok.clear()
                self.textBrowser_temp_krok.append(str(krok))
                self.nowe_dane()
                self.rysuj_wykres()

    def nowe_dane(self):
        self.textBrowser_rozw.append("\nKrok: " + str(krok))
        tekst="Współrzędne wyznaczonego punktu optymalnego: x = [ "
        for i in range(int(Alg.ile_zmiennych(Alg.wzor))+1):
            tekst = tekst + str(Alg.tablica_wynikow[krok - 1][i]) + " "
            if i == int(Alg.ile_zmiennych(Alg.wzor))-1:
                self.textBrowser_rozw.append(tekst + "]")
            elif i > int(Alg.ile_zmiennych(Alg.wzor))-1:
                self.textBrowser_rozw.append("f(x)=" + str(Alg.tablica_wynikow[krok - 1][i]))
        #self.textBrowser_rozw.append("f(x) = "+str(Alg.tablica_wynikow[krok - 1][(int(Alg.ile_zmiennych(Alg.wzor))+1)]))
        self.textBrowser_rozw.append("Największa odległość między dwoma punktami simpleksu: " + str(Alg.tablica_wynikow[krok - 1][int(Alg.ile_zmiennych(Alg.wzor))+1]))
        self.textBrowser_ilosc_krok.append(str(krok))

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()