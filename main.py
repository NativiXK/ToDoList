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
from unicodedata import name
from PyQt5.QtWidgets import (
    QApplication, 
    QSystemTrayIcon, 
    QAction,
    QStylePainter,
    QMenu, 
    QWidget, 
    QLabel, 
    qApp, 
    QStyleOption,
    QStyle,
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
    This class implements the main windows of the app.
    """

    def __init__(self, title : str, description : str, callback : object, geometry : tuple) -> None:
        super(Landing, self).__init__()
        self.setObjectName("Landing")
        self.title = title
        self.description = description
        self.callback = callback
        self.geometry = geometry
        self.__main_layout = QVBoxLayout()
        self.initUI()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption();
        opt.initFrom(self)
        p = QStylePainter(self);
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self);

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.geometry[0], self.geometry[1], self.geometry[2], self.geometry[3])
        self.setWindowIcon(QtGui.QIcon("open-book.png"))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(self.geometry[2], self.geometry[3])
        self.setMaximumSize(self.geometry[2], self.geometry[3])
        self.update_cards()
        
        self.show()

    def update_cards(self, cards : list = []) -> None:
        """
        Receives a list card layouts to be added to the main layout
        """
        
        self.__main_layout.addWidget(Card(1, "Mateus Konkol", "21/04/2022","É um cara esforçado para aprender as coisas no mundo e se dedicar a sua noiva Lavininha", self.callback))

        self.setLayout(self.__main_layout)

    def closeEvent(self, event) -> None:
        self.hide()
        event.ignore()

class Card(QWidget):
    """
    This class inherits from QWidget and implements a card layout
    """

    def __init__(self, id : int, title : str, date : str, description : str, callback : object) -> None:
        super(Card, self).__init__()
        self.setObjectName("card") #Sets the object name to be used in stylesheets
        self.__id : int = id
        self.__title : str = title
        self.__description : str = description
        self.__date : str = date

        header = QHBoxLayout()
        header.setObjectName("card-header-layout")
        header.addWidget(QLabel(title), alignment=QtCore.Qt.AlignRight)
        header.addWidget(QLabel(date), alignment=QtCore.Qt.AlignLeft)

        button = QPushButton("Concluído")
        button.setObjectName("card-button")

        self.__card = QVBoxLayout()
        self.__card.setObjectName("card-layout")
        self.__card.addLayout(header)
        self.__card.addWidget(QLabel(description), alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__card.addWidget(button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.__card)
        self.mousePressEvent = self.__mousePressEvent

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption();
        opt.initFrom(self)
        p = QStylePainter(self);
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self);

    def __mousePressEvent(self, event) -> None:
        print("Você clicou neste card")

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
        self.app.setStyle("Fusion")
        self.tray = TraySystem(self.menu)
        self.landing = Landing("To Do List", "Aqui você pode criar sua lista de tarefas", self, self.geometry)
        self.app.setStyleSheet("""
QWidget#Landing {
    background-color: #a6a6a6;
}

QWidget#card {

    background-color: #cccccc;
    border-radius: 10px;
    margin: 5%;
    padding: 5%;
    border: 1px solid gray;
    max-height: 10em;
}

QWidget#card:pressed {
    background-color: #9fcf40;
}

QPushButton#card-button {
    background-color: #b0b0b0;
    border-width: 2px;
    border-radius: 5px;
    border-color: beige;
    font: bold 14px;
    width: 100px;
    height: 30px;
    padding: 2%;
}

QPushButton#card-button:hover {
    background-color: #a6a6a6;
    border: 1px solid gray;
    border-style: outset;
}
        """)
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
