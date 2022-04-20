"""
Project: To Do List App
Description: 
Por: Mateus Konkol
Data: 03/2021

"""

from asyncio import events
from re import A
import sys, ctypes
import tkinter
from PyQt5.QtWidgets import (
    QApplication, 
    QShortcut, 
    QSystemTrayIcon, 
    QAction, 
    QMenu, 
    QWidget, 
    QLabel, 
    qApp, 
    QLayout, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton,
    )

from PyQt5 import QtCore, QtGui

class TraySystem(QSystemTrayIcon):
    """
    This class allows controlling a system tray icon, by passing a dictionary of the menu strcture and their callback functions.
    if a menu has None value, it will generate a separator.
    """

    def __init__(self, menu_callback):
        
        super().__init__()
        self.menu_actions : list = menu_callback
        
        QSystemTrayIcon.__init__(self) #Inicializa o app no sistema tray

        # Set icon to a standard or custom icon
        self.setIcon(QtGui.QIcon("open-book.png"))
        self.setToolTip("To Do List")
        
        #Bind events
        self.messageClicked.connect(self.showMenu) #Linka o signal gerado ao clicar na menssagem para exibir o menu
        self.activated.connect(self.showMenu) #Linka o signal gerado ao clicar no icone para exibir o menu

        self.tray_menu = QMenu("CTo Do List")
        self.updateMenu()

    def updateMenu(self):
        """
        Update the menu with the new menu structure
        """
        self.tray_menu.clear()
        for menu_item in self.menu_actions:
            if menu_item[1] == "separator":
                self.tray_menu.addSeparator()
                continue
            elif menu_item[1] == "text":
                self.tray_menu.addAction(menu_item[0])
                continue
            else:
                self.tray_menu.addAction(menu_item[0], menu_item[1])

        self.setContextMenu(self.tray_menu)  # Set right-click menu
        self.show()

    #Exibe menu após clicar na mensagem
    def showMenu(self):
        self.updateMenu()
        self.tray_menu.popup(QtGui.QCursor.pos())
        self.tray_menu.showNormal()

    def notify(self, message):
        """Generate a desktop notification"""
        self.showMessage(   "Atenção",
                            message + "\nClique para selecionar ação",
                            QSystemTrayIcon.Information,
                            5    )

    def notifyError(self, message):
        self.showMessage(   "Erro",
                            message,
                            QSystemTrayIcon.Warning,
                            5    )

    def exitApp(self):
        self.hide()
        qApp.quit()

class Landing(QWidget):
    """
    This class represents a card with a title and a description.
    """

    def __init__(self, title : str, description : str, callback : object, geometry : tuple) -> None:
        super().__init__()
        self.title = title
        self.description = description
        self.callback = callback
        self.geometry = geometry
        self.__main_layout = QVBoxLayout()
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.geometry[0], self.geometry[1], self.geometry[2], self.geometry[3])
        self.setWindowIcon(QtGui.QIcon("open-book.png"))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #f2f2f2;")
        self.setMinimumSize(self.geometry[2], self.geometry[3])
        self.setMaximumSize(self.geometry[2], self.geometry[3])
        self.update()
        
        self.show()

    def update(self, cards : list = []) -> None:
        """
        Receives a list card layouts to be added to the main layout
        """

        header = QHBoxLayout()
        title = QLabel("Titulo")
        date = QLabel("Data")
        header.addWidget(title)
        header.addWidget(date)
        description = QLabel("Descrição: \n Lorem ipsum gravida taciti elit dui vehicula iaculis habitasse imperdiet hac, vivamus velit accumsan et odio sem nibh nulla id pellentesque hac, donec sollicitudin sapien tortor vivamus integer aenean eros nisl.")
        done_button = QPushButton("Concluído")
        t = QWidget()

        card = QVBoxLayout()
        card.addLayout(header)
        card.addWidget(description, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        card.addWidget(done_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        t.setLayout(card)
        t.setFixedSize(self.geometry[3] - 30,200)
        t.setContentsMargins(20,20,20,20)
        t.setStyleSheet("background-color: white;")

        self.__main_layout.addWidget(t)

        self.setLayout(self.__main_layout)

    def closeEvent(self, event) -> None:
        self.hide()
        event.ignore()

class CardLayout(QLayout):

    def __init__(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

    def addItem(self, item):
        pass

class App:

    def __init__(self) -> None:
        self.menu = [
            ("Abrir", self.open_list),
            ("Separador", "separator"),
            ("Configurar", self.configurar),
            ("Sair", self.exit)
        ]
        self.__user32 = ctypes.windll.user32
        self.screen_resolution : tuple = (self.__user32.GetSystemMetrics(0), self.__user32.GetSystemMetrics(1))
        self.width : int = 500
        self.height : int = 800
        self.geometry = (int(self.screen_resolution[0] / 2 - self.width / 2), int(self.screen_resolution[1] / 2 - self.height / 2), self.width, self.height)

    def run(self):

        self.app = QApplication(sys.argv)
        self.tray = TraySystem(self.menu)
        self.landing = Landing("To Do List", "Aqui você pode criar sua lista de tarefas", self, self.geometry)
        self.app.exec_()

    def open_list(self):
        self.landing.show()

    def configurar(self):
        print("Configurar")

    def exit(self):
        self.tray.exitApp()
        
if __name__ == "__main__":
    app = App()
    
    try:
        app.run()
    except Exception as e:
        print(e)
        app.exit()
