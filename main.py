
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QDesktopWidget, \
    QHBoxLayout, QLabel, QVBoxLayout, QSystemTrayIcon


class controler_linux():

    def __init__(self):
        print('classe intanciada')


    def valor_brilho_atual(self):
        file_brilho_atual = open("/sys/class/backlight/intel_backlight/brightness", "r")
        brilho = int(file_brilho_atual.read())
        file_brilho_atual.close()
        return brilho


    def aumentar(self):

        file_brilho_maximo = open("/sys/class/backlight/intel_backlight/max_brightness", 'r')
        valor_maximo = int(file_brilho_maximo.read())
        file_brilho_maximo.close()

        file_brilho_atual = open("/sys/class/backlight/intel_backlight/brightness", "w+")


        brilho = int(file_brilho_atual.read()) + 285

        if (brilho <= valor_maximo):
            file_brilho_atual.write("%s" %(brilho))
            print('brilho aumentado para ', brilho)
        else:
            file_brilho_atual.write("%s" %(valor_maximo))
            return True

        file_brilho_atual.close()
        return False



    def diminuir(self):

        valor_minimo = 287

        file_brilho_atual = open("/sys/class/backlight/intel_backlight/brightness", "w+")

        brilho = int(file_brilho_atual.read()) - 285

        if (brilho >= valor_minimo):
            file_brilho_atual.write("%s" %(brilho))
            print('brilho diminuido para ', brilho)
        else:
            file_brilho_atual.write("%s" %(valor_minimo))
            return True


        file_brilho_atual.close()
        return False



class Janela(QMainWindow):


    # contrutor
    def __init__(self):
        super(Janela, self).__init__()
        self.title = 'Ajustar Brilho'
        self.width = 300
        self.height = 150
        self.initUI()

    #
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # Controle do brilhho
        self.controle_brilho = controler_linux()

        # container
        self.container()

        # Status Bar
        self.configure_status_bar()

        self.setWindowIcon(QIcon("ajustar_brilho.png"))

        # centralizar a janela
        self.center()


    def atualizar_brilho(self,opcao):
        if opcao is True:
            if self.controle_brilho.aumentar():
                self.status_bar.showMessage("Limite de Brilho Máximo Configurado")
        else:
            if self.controle_brilho.diminuir():
                self.status_bar.showMessage("Limite de Brilho Minímo Configurado")

        self.info_brilho.setText(str('Brilho Atual [ ') + str(self.controle_brilho.valor_brilho_atual()) + ' ]')




    def container(self):

        container = QWidget(self)
        self.setCentralWidget(container)
        layout = QVBoxLayout()

        self.info_brilho = QLabel()
        self.info_brilho.setText(str('Brilho Atual [ ')+str(self.controle_brilho.valor_brilho_atual())+' ]')
        self.info_brilho.setAlignment(Qt.AlignCenter)
        self.info_brilho.setStyleSheet("background-color:rgb(100, 100, 100)")

        layout_label = QHBoxLayout()
        layout_label.addWidget(self.info_brilho)


        self.diminuir_brilho = QPushButton()
        self.diminuir_brilho.setText(" Diminuir [ - ] ")
        self.diminuir_brilho.clicked.connect(lambda: self.atualizar_brilho(False))

        self.aumentar_brilho = QPushButton()
        self.aumentar_brilho.setText(" [ + ] Aumentar  ")
        self.aumentar_brilho.clicked.connect(lambda: self.atualizar_brilho(True))


        layout_bt = QHBoxLayout()
        layout_bt.addWidget(self.diminuir_brilho)
        layout_bt.addWidget(self.aumentar_brilho)


        layout.addLayout(layout_label)
        layout.addLayout(layout_bt)
        container.setLayout(layout)



    # STATUS BAR
    def configure_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('this is status bar')
        self.status_bar.setStyleSheet("background-color:rgb(100, 100, 100)")


    # posicona a janela no cento
    def center(self):
        qr = self.frameGeometry() ## geometry of the main window
        cp = QDesktopWidget().availableGeometry().center() # center point of screen
        qr.moveCenter(cp) # # move rectangle's center point to screen's center point
        self.move(qr.topLeft()) # # top left of rectangle becomes top left of window centering it


if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("input parameters = " + str(sys.argv))
    tutorial_window = Janela()
    tutorial_window.show()
    sys.exit(app.exec_())