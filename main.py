"""
Project: To Do List App
Description: 
Por: Mateus Konkol
Data: 03/2021

"""

import sys
import ctypes
import utils.styles as styles
import utils.dbConnector as db

from PyQt5.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QTimer,
    QEasingCurve,
)

from PyQt5.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMainWindow,
    QStylePainter,
    QMenu,
    QFrame,
    QWidget,
    QLabel,
    qApp,
    QStyleOption,
    QStyle,
    QVBoxLayout, 
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QGraphicsDropShadowEffect,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QComboBox,
)

from PyQt5 import QtCore, QtGui

class TraySystem(QSystemTrayIcon):
    """
    This class allows controlling a system tray icon, by passing a dictionary of the menu strcture and their callback functions.
    if a menu has None value, it will generate a separator.
    """

    def __init__(self, menu_callback, callback : object):
        
        super().__init__()
        self.menu_actions : list = menu_callback
        self.__callback = callback
        QSystemTrayIcon.__init__(self) #Inicializa o app no sistema tray

        self.doubleTimer = QTimer()
        self.doubleTimer.setSingleShot(True)
        self.doubleTimer.timeout.connect(self.showMenu)

        # Set icon to a standard or custom icon
        self.setIcon(QtGui.QIcon("open-book.png"))
        self.setToolTip("To Do List")
        
        #Bind events
        # self.messageClicked.connect(self.showMenu) #Linka o signal gerado ao clicar na menssagem para exibir o menu
        self.activated.connect(self.click) #Linka o signal gerado ao clicar no icone para exibir o menu

        self.tray_menu = QMenu("To Do List")
        self.updateMenu()
        self.show()

    def click(self):

        if self.doubleTimer.isActive():
            self.__callback.open_list()
            self.doubleTimer.stop()
        else:
            self.doubleTimer.start(150)

    def updateMenu(self):
        """
        Update the menu with the new menu structure
        """
        self.tray_menu.clear()

        menu = self.menu_actions

        for menu_item in menu:
            # print(menu_item)
            if menu_item[1] == "separator":
                self.tray_menu.addSeparator()
                
            elif menu_item[1] == "text":
                self.tray_menu.addAction(menu_item[0])
            
            elif type(menu_item) == list:
                menu = self.tray_menu.addMenu(menu_item[0])
                for submenu in menu_item[1:]:
                    menu.addAction(submenu[0], submenu[1])

            else:
                self.tray_menu.addAction(menu_item[0], menu_item[1])

        # self.setContextMenu(self.tray_menu)  # Set right-click menu
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
        self.__callback.exit()

class Landing(QWidget):
    """
    This class implements the main windows of the app.
    """

    def __init__(self, title : str, description : str, callback : object, geometry : tuple, cards: list = []) -> None:
        super(Landing, self).__init__()
        self.title = title
        self.description = description
        self.callback = callback
        self.geometry = geometry
        self.__cards : list = self.__build_cards(cards)
        # self.__cards.append(Card(id = 1, title = "Lavar o carro", description = "Comprar produtos", callback = self))
        # self.__cards.append(Card(id = 2, title = "Limpar o tênis", date="22/05/2022", callback = self))
        # self.__cards.append(Card(id = 3, title = "Lavar a louça", callback = self))
        # self.__cards.append(Card(id = 4, title = "Levar DOG no pet", date="17/05/2022", description="apenas banho e tosa higiênica", callback = self))

        self.initUI()

    def __build_cards(self, tasks : list) -> list:
        # print(tasks)
        return [Card(id = card["id"], title = card["title"], date = card["date"], description = card["description"], status = card["status"],callback=self) for card in tasks]

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def initUI(self) -> None:
        #Set main window properties
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(self.geometry[0], self.geometry[1], self.geometry[2], self.geometry[3])
        self.setWindowIcon(QtGui.QIcon("open-book.png"))
        #set border radius in the main window

        self.setMinimumSize(self.geometry[2], self.geometry[3])
        self.setMaximumSize(self.geometry[2], self.geometry[3])

        self.setObjectName("Landing")

        self.header = Header(self.title, self)
        self.menu = Menu(self)
        self.card_list = CardList()
        self.footer = Footer(self)

        #Set an empty layout to the main window
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 5)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.layout().addWidget(self.header)
        self.layout().addWidget(self.menu)
        self.layout().addWidget(self.card_list)
        self.layout().addWidget(self.footer)

        self.card_list.update_cards(self.__cards)

        self.show()

    def toggle_menu(self):
        self.menu.state = not self.menu.state

    def add_card(self) -> None:
        new = CardEditor(Card(id = len(self.__cards) + 1, callback = self), True, self)
        self.card_list.update_cards([new])
        self.open_card_editor(new)

    def save_card(self, editor : object) -> None:

        card = editor.get_card()
        if not card in self.__cards:
            self.__cards.insert(0, card)
            self.callback.new_task(str(card))
        else:
            self.callback.save_task(str(card))

        self.close_card_editor(editor)
        
    def open_card(self, card : object) -> None:
        editor = CardEditor(card, False, self)
        self.card_list.update_cards([editor])
        self.open_card_editor(editor)

    def open_card_editor(self, editor : object) -> None:
        editor.animation = QPropertyAnimation(editor, b"maximumHeight")
        editor.animation.setStartValue(0)
        editor.animation.setEndValue(editor.height())
        editor.animation.setDuration(200)
        editor.animation.setEasingCurve(QEasingCurve.InOutCubic)
        editor.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def close_card_editor(self, editor : object) -> None:
        editor.animation = QPropertyAnimation(editor, b"maximumHeight")
        editor.animation.setStartValue(editor.height())
        editor.animation.setEndValue(0)
        editor.animation.setDuration(200)
        editor.animation.setEasingCurve(QEasingCurve.InOutCubic)
        editor.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        editor.animation.finished.connect(lambda: self.card_list.update_cards(self.__cards))
        
    def card_done(self, card : object) -> None:
        card.status = 1
        self.callback.save_task(str(card))

        card.anim_height = QPropertyAnimation(card, b"maximumHeight")
        card.anim_height.setStartValue(card.height())
        card.anim_height.setEndValue(0)
        card.anim_height.setDuration(150)
        card.anim_height.setEasingCurve(QEasingCurve.InOutCubic)

        card.anim_width = QPropertyAnimation(card, b"maximumWidth")
        card.anim_width.setStartValue(card.width())
        card.anim_width.setEndValue(0)
        card.anim_width.setDuration(250)
        card.anim_width.setEasingCurve(QEasingCurve.InOutCubic)

        card.animation = QParallelAnimationGroup()
        card.animation.addAnimation(card.anim_height)
        card.animation.addAnimation(card.anim_width)
        card.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        card.animation.finished.connect(lambda: card.setParent(None))

    def delete_card(self, card : object) -> None:

        card.status = 2 # Deleted card
        self.callback.save_task(str(card))
        self.card_list.update_cards(self.__cards)

    def update_cards(self):
        self.__cards = self.__build_cards(self.callback.tasks())
        # for card in self.__cards:
        #     card.status = 0
        self.card_list.update_cards(self.__cards)

    def closeEvent(self, event) -> None:
        self.hide()
        event.ignore()

class Card(QWidget):
    """
    This class inherits from QWidget and implements a card layout 

    Status:
        0 - Open
        1 - Done
        2 - "Deleted"
    """

    def __init__(self, id : int = 0, title : str = "", date : str = "", description : str = "", status : int = 0, callback : object = None) -> None:
        super(Card, self).__init__()
        self.setObjectName("card") #Sets the object name to be used in stylesheets
        self.__id : int = id
        self.__title : str = title
        self.__description : str = description
        self.__date : str = date
        self.__status : str = status
        self.__callback = callback
        self.setLayout(QGridLayout())
        self.__buildLayout()

    def __str__(self) -> str:
        return f"({self.id}, \"{self.title}\", \"{self.date}\", \"{self.description}\", {self.status})"

    def __buildLayout(self) -> None:
        
        self.enterEvent = self.__enter_card
        self.leaveEvent = self.__leave_card

        layout = self.layout()

        #card.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel(self.__title)
        label.setObjectName("card-title")
        label.setFont(styles.fonts[label.objectName()])
        
        if self.__description:
            layout.addWidget(label, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft)
        elif self.__date: 
            layout.addWidget(label, 0, 0, 2, 2, QtCore.Qt.AlignmentFlag.AlignLeft)
            
        else:
            layout.addWidget(label, 0, 0, 2, 4, QtCore.Qt.AlignmentFlag.AlignLeft)

        label = QLabel(self.__date)
        label.setObjectName("card-date")
        label.setFont(styles.fonts[label.objectName()])

        if self.__description:
            layout.addWidget(label, 0, 2, 1, 2, QtCore.Qt.AlignmentFlag.AlignRight)
        elif self.__date:
            layout.addWidget(label, 0, 2, 2, 2, QtCore.Qt.AlignmentFlag.AlignRight)



        if self.__description:
            label = QLabel(self.__description)
            label.setWordWrap(True)
            label.setObjectName("card-description")
            label.setFont(styles.fonts[label.objectName()])
            layout.addWidget(label, 1, 0, 1, 4)

        button = QPushButton("Concluído")
        button.setObjectName("card-button")
        button.setFont(styles.fonts[button.objectName()])
        button.clicked.connect(lambda : self.__callback.card_done(self))
        layout.addWidget(button, 2, 0, 1, 4)

        self.mousePressEvent = self.__mousePressEvent

    def __clear(self):
        layout = self.layout()

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def date(self) -> str:
        return self.__date

    @property
    def status(self) -> str:
        return self.__status

    @title.setter
    def title(self, value : str) -> None:
        self.__title = value
    
    @date.setter
    def date(self, value : str) -> None:
        self.__date = value
    
    @description.setter
    def description(self, value : str) -> None:
        self.__description = value
    
    @status.setter
    def status(self, value : str) -> None:
        self.__status = value

    def rebuildLayout(self):

        self.__clear()
        self.__buildLayout()

    def __enter_card(self, event) -> None:
        hover = QGraphicsDropShadowEffect()
        hover.setOffset(4, 4)
        hover.setBlurRadius(10)
        self.setGraphicsEffect(hover)

    def __leave_card(self, event):
        self.setGraphicsEffect(None)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def __mousePressEvent(self, event) -> None:
        self.__callback.open_card(self)

class CardEditor(QWidget):
    """
    Receives a card and builds a card editor, allowing to change the card's title, date, description and status.
    Also, it allows to delete the card, save changes and close the editor.
    """

    def __init__(self, card : object, new : bool, callback : object) -> None:
        super(CardEditor, self).__init__()
        self.setObjectName("card-editor") #Sets the object name to be used in stylesheets
        self.__card = card
        self.__callback = callback
        self.__layout = QGridLayout()
        self.__build(new)

    def __build(self, new : bool) -> None:

        self.__back = QPushButton("Voltar")
        self.__back.setObjectName("card-editor-back")
        self.__back.setFont(styles.fonts[self.__back.objectName()])
        self.__back.clicked.connect(lambda : self.__callback.close_card_editor(self))
        self.__layout.addWidget(self.__back, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

        if not new:
            self.__delete = QPushButton("Deletar")
            self.__delete.setObjectName("card-editor-delete")
            self.__delete.setFont(styles.fonts[self.__delete.objectName()])
            self.__delete.clicked.connect(lambda : self.__callback.delete_card(self.__card))
            self.__layout.addWidget(self.__delete, 0, 4, 1, 2, QtCore.Qt.AlignmentFlag.AlignRight)

        self.__titleLabel = QLabel("Título:")
        self.__titleLabel.setObjectName("card-title")
        self.__titleLabel.setFont(styles.fonts[self.__titleLabel.objectName()])
        self.__layout.addWidget(self.__titleLabel, 1, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.__title = QLineEdit(self.__card.title)
        self.__title.setObjectName("card-editor-title")
        self.__title.setFont(styles.fonts[self.__title.objectName()])
        self.__layout.addWidget(self.__title, 2, 0, 1, 3)

        self.__dateLabel = QLabel("Data:")
        self.__dateLabel.setObjectName("card-date")
        self.__dateLabel.setFont(styles.fonts[self.__dateLabel.objectName()])
        self.__layout.addWidget(self.__dateLabel, 1, 4, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.__date = QLineEdit(self.__card.date)
        self.__date.setObjectName("card-editor-date")
        self.__date.setFont(styles.fonts[self.__date.objectName()])
        self.__layout.addWidget(self.__date, 2, 4, 1, 2)

        self.__descriptionLabel = QLabel("Descrição:")
        self.__descriptionLabel.setObjectName("card-date")
        self.__descriptionLabel.setFont(styles.fonts[self.__descriptionLabel.objectName()])
        self.__layout.addWidget(self.__descriptionLabel, 3, 0, 1, 6, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.__description = QTextEdit(self.__card.description)
        self.__description.setObjectName("card-editor-description")
        self.__description.setFont(styles.fonts[self.__description.objectName()])
        self.__layout.addWidget(self.__description, 4, 0, 2, 6, alignment = QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__save = QPushButton("Salvar")
        self.__save.setObjectName("card-editor-save")
        self.__save.setFont(styles.fonts[self.__save.objectName()])
        self.__save.clicked.connect(self.saveCard)
        self.__layout.addWidget(self.__save, 6, 0, 1, 6, QtCore.Qt.AlignmentFlag.AlignJustify)

        self.setLayout(self.__layout)
        self.adjustSize()        

    def saveCard(self):
        if self.__title.text():
            self.__callback.save_card(self)
        else:
            QMessageBox.about(self.__callback, "Falta informação", "Adicione ao menos um título à tarefa")

    def get_card(self) -> None:
        self.__card.title = self.__title.text()
        self.__card.date = self.__date.text()
        self.__card.description = self.__description.toPlainText()
        self.__card.rebuildLayout()
        return self.__card

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class Menu(QWidget):

    def __init__(self, callback) -> None:
        super(Menu, self).__init__()
        self.callback = callback
        self.__state = False
        self.max_height = 200;

        self.setHidden(True)

        self.setObjectName("menu")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(100, 10, 100, 10)
        self.layout().setSpacing(10)

        self.geometry().setHeight(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        self.button = QPushButton(self, text="Tarefas finalizadas")
        self.button.setObjectName("menu-button")
        self.button.setFont(styles.fonts[self.button.objectName()])
        self.layout().addWidget(self.button)

        self.button = QPushButton(self, text="Tarefas excluídas")
        self.button.setObjectName("menu-button")
        self.button.setFont(styles.fonts[self.button.objectName()])
        self.layout().addWidget(self.button)

        self.adjustSize()
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state : bool):
        if state:
            self.__open()
        else:
            self.__close()

    def __open(self):
        self.__state = True
        startGeom = self.geometry()
        # endGeom = QtCore.QRect(startGeom.left(), startGeom.top(), startGeom.width(), 200)
        self.setHidden(False)
        self.animation = QPropertyAnimation(self, b"maximumHeight")
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.max_height)
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

        # open = lambda : self.setFixedHeight(self.max_height)

        self.animation.finished.connect(lambda: self.repaint())
    
    def __close(self):
        self.__state = False
        startGeom = self.geometry()
        # endGeom = QtCore.QRect(startGeom.left(), startGeom.top(), startGeom.width(), int(0))

        self.animation = QPropertyAnimation(self, b"maximumHeight")
        self.animation.setStartValue(self.max_height)
        self.animation.setEndValue(0)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        
        # close = lambda : self.setFixedHeight(0)

        self.animation.finished.connect(lambda: self.repaint())

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class Header(QWidget):

    def __init__(self, title : str, callback : QMainWindow) -> None:
        super(Header, self).__init__()
        self.setObjectName("header")
        self.__title = title
        self.callback = callback
        self.__build()

    def __build(self) -> None:
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        
        self.menuButton = QPushButton(parent = self, text="MENU")
        self.menuButton.setObjectName("header-menu-button")
        self.menuButton.clicked.connect(lambda : self.callback.toggle_menu())

        self.titleLabel = QLabel(parent = self, text = self.__title)
        self.titleLabel.setObjectName("header-title")
        self.titleLabel.setFont(styles.fonts[self.titleLabel.objectName()])

        self.closeButton = QPushButton(parent = self, text = "X")
        self.closeButton.setObjectName("header-close-button")
        self.closeButton.setFont(styles.fonts[self.closeButton.objectName()])
        self.closeButton.clicked.connect(lambda : self.callback.close())

        header.addWidget(self.menuButton)
        header.addWidget(self.titleLabel)
        header.addWidget(self.closeButton)

        self.setLayout(header)

    @property
    def title(self) -> str:
        return self.titleLabel.text()
    
    @title.setter
    def title(self, title : str) -> None:
        self.titleLabel.setText(title)
        self.__title = title

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class Footer(QWidget):

    def __init__(self, callback : object) -> None:
        super(Footer, self).__init__()
        self.__callback = callback
        self.setObjectName("footer")
        self.__build()

    def __build(self) -> None:
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 0, 0, 0)

        self.addButton = QPushButton(parent = self, text = "Adicionar")
        self.addButton.setObjectName("footer-add-button")
        self.addButton.setFont(styles.fonts[self.addButton.objectName()])
        self.addButton.clicked.connect(lambda : self.__callback.add_card())

        footer.addWidget(self.addButton)

        self.setLayout(footer)

class CardList(QScrollArea):

    def __init__(self) -> None:
        super(CardList, self).__init__()
        self.setObjectName("card-list") #Sets the object name to be used in stylesheets
        self.widget = QWidget(self)

        self.__list_layout = QVBoxLayout()
        self.__list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.widget.setLayout(self.__list_layout)
 
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        #Remove vertical scrollbar
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QScrollArea.NoFrame)

    def clean(self) -> None:
        """
        Removes all cards from the list
        """
        for i in reversed(range(self.__list_layout.count())):
            self.__list_layout.itemAt(i).widget().setParent(None)

    def update_cards(self, cards : list = []) -> None:
        """
        Receives a list card layouts to be added to the main layout
        """
        layout = self.__list_layout
        self.clean()

        for card in cards:
            if type(card) == Card:
                if card.status == 0:
                    layout.addWidget(card)
            if type(card) == CardEditor:
                layout.addWidget(card)
        
        # print(layout.count())

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        This function must exist in order to use the stylesheets
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QStylePainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

class App:

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.menu = [
            ("Abrir", self.open_list),
            ("Separador", "separator"),
            [
                "Configurações", # Submenu title
                ("Atualizar lista", self.update_cards),
                ("Limpar tudo", self.clearAllTasks),
                ("Configurar", self.settings),
            ],
            ("Sair", self.exit)
        ]

        self.conn = db.Connector(path="tasks.db", schema="schema.sql")
        self.__user32 = ctypes.windll.user32
        self.screen_resolution : tuple = (self.__user32.GetSystemMetrics(0), self.__user32.GetSystemMetrics(1))
        self.width : int = 500
        self.height : int = 700
        self.geometry = (int(self.screen_resolution[0] / 2 - self.width / 2), int(self.screen_resolution[1] / 2 - self.height/2 - 25), self.width, self.height) 

    def tasks(self):
        return self.conn.tasks()

    def new_task(self, task : str):
        task = "(" + ",".join(task.strip("()").split(",")[1:]) + ")"
        self.conn.add_task(task)

    def save_task(self, task : str):
        self.conn.update_task(task)

    def run(self):
        self.app.setStyle("Fusion")
        self.tray = TraySystem(self.menu, self)
        self.landing = Landing("To Do List", "Aqui você pode criar sua lista de tarefas", self, self.geometry, cards=self.tasks())
        
        self.app.setStyleSheet(styles.stylesheet)
        
        self.app.exec_()

    def open_list(self):

        self.landing.show()

    def settings(self):
        print("Settings")
    
    def clearAllTasks(self):
        self.conn.reinit()
        self.landing.update_cards()

    def update_cards(self):
        self.landing.update_cards()

    def exit(self):
        self.app.quit()
        
if __name__ == "__main__":
    app = App()
    
    try:
        app.run()
    except Exception as e:
        print(e)
        app.exit()
