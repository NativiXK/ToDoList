"""
Project: To Do List App
Description: 
Por: Mateus Konkol
Data: 03/2021

"""

from asyncio import events
from re import A
import sys
import tkinter
from PyQt5.QtWidgets import QApplication, QShortcut, QSystemTrayIcon, QAction, QMenu, QWidget, QLabel, qApp
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

    def __init__(self, title, description, callback):
        super().__init__()
        self.title = title
        self.description = description
        self.callback = callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(QtGui.QIcon("open-book.png"))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #f2f2f2;")


        # self.title_label = QLabel(self, text=self.title, font=("Arial", 16))
        # self.title_label.pack(side="top", fill="x", pady=10)

        # self.description_label = QLabel(self, text=self.description, font=("Arial", 12))
        # self.description_label.pack(side="top", fill="x", pady=10)

        # self.button = tkinter.Button(self, text="OK", command=self.callback)
        # self.button.pack(side="top", fill="x", pady=10)

        self.show()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.hide()
        event.ignore()

class App:

    def __init__(self) -> None:
        self.menu = [
            ("Olá", "text"),
            ("Abrir", self.open_list),
            ("Separador", "separator"),
            ("Configurar", self.configurar),
            ("Sair", self.exit)
        ]

    def run(self):

        self.app = QApplication(sys.argv)
        self.tray = TraySystem(self.menu)
        self.app.exec_()

    def open_list(self):
        self.landing = Landing("To Do List", "Aqui você pode criar sua lista de tarefas", self.hide_landing)

    def hide_landing(self):
        self.landing.hide()

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
