from PyQt5.QtGui import QFont


fonts = {
    "card-title" : QFont("Helvetica", 12, QFont.Bold),
    "card-date" : QFont("Helvetica", 12, QFont.Bold),
    "card-description" : QFont("Helvetica", 10, QFont.Normal),
    "card-button" : QFont("Helvetica", 12, QFont.Bold),
    "header-title" : QFont("Helvetica", 14, QFont.Bold),
    "header-close-button" : QFont("Helvetica", 14, QFont.Bold),
    "card-editor-title" : QFont("Helvetica", 12, QFont.Bold),
    "card-editor-back" : QFont("Helvetica", 12, QFont.Bold),
    "card-editor-description" : QFont("Helvetica", 12, QFont.Normal),
    "card-editor-date" : QFont("Helvetica", 12, QFont.Bold),
    "card-editor-save" : QFont("Helvetica", 12, QFont.Bold),
    "card-editor-delete" : QFont("Helvetica", 12, QFont.Bold),
    "footer-delete-button" : QFont("Helvetica", 12, QFont.Bold),
    "footer-delete-button" : QFont("Helvetica", 12, QFont.Bold),
    "footer-add-button" : QFont("Helvetica", 12, QFont.Bold),
    "footer-delete-button" : QFont("Helvetica", 12, QFont.Bold),
}

stylesheet = """
QWidget#Landing {
    background-color: white;
    border-radius: 10px;
}

QWidget#card {

    background-color: #cccccc;
    border-radius: 10px;
    padding: 0px;
    margin: 5px;
    border: 1px solid gray;
    max-height: 15em;
    max-width: 500px;
}

QWidget#card:hover {
    background-color: #cfcfcf;
}

QPushButton#card-button {
    background-color: #b0b0b0;
    border-width: 2px;
    border-radius: 5px;
    border-color: beige;
    width: 100px;
    height: 40px;
}

QPushButton#card-button:hover {
    background-color: #a6a6a6;
    border: 1px solid gray;
    border-style: outset;
}

#card-title, #card-date {
    text-align: center;
    margin: 10px;
}

#card-description {
    text-align: justify;
    margin: 0 5px 0 5px;
}

QWidget#header {
    background-color: #cccccc;
    border: 1px solid gray;
    min-height: 40px;
}

QLabel#header-title {
    margin: 5px 0 5px 10px;
}

QPushButton#header-close-button {
    background-color: red;
    border-width: 2px;
    border-radius: 15px;
    margin: 5px 10px 5px 0;
    max-width: 40px;
    max-height: 40px;
}

QPushButton#header-close-button:hover {
    background-color: #c91100;
    min-width: 45px;
    min-height: 45px;
}

QPushButton#card-editor-back {
    background-color: #b0b0b0;
    border-width: 2px;
    border-radius: 5px;
    border-color: beige;
    min-width: 150px;
    min-height: 40px;
}

QPushButton#card-editor-back:hover {
    background-color: #a6a6a6;
    border: 1px solid gray;
    border-style: outset;
}

QPushButton#card-editor-delete {
    background-color: red;
    border-width: 2px;
    border-radius: 5px;
    margin: 5px 0px 5px 0;
    min-width: 150px;
    min-height: 40px;
}

QPushButton#card-editor-delete:hover {
    background-color: #c91100;
    border: 1px solid gray;
    border-style: outset;
}

QPushButton#card-editor-save {
    background-color: #b0b0b0;
    border-width: 2px;
    border-radius: 5px;
    margin: 5px 0px 5px 0;
    min-width: 200px;
    min-height: 40px;
}

QPushButton#card-editor-save:hover {
    background-color: #a6a6a6;
    border: 1px solid gray;
    border-style: outset;
}

QLineEdit#card-editor-title, QLineEdit#card-editor-date {
    min-height: 35px;
}

QLineEdit#card-editor-title, QLineEdit#card-editor-date{
    border-bottom-color: gray;
    border-bottom: 5px;
}

QLineEdit#card-editor-title:focus{
    border-bottom-color: blue;
    border-bottom: 50px;
}

QWidget#footer {
    background-color: #cccccc;
    max-height: 40px;
    margin: 0 5px 0 5px;
    padding: 0px;
}

QPushButton#footer-add-button {
    background-color: #b0b0b0;
    min-height: 40px;
    min-width: 100%;
    margin: 0 5px 0 5px;
    padding: 0px;
    border-radius: 5px;
}

#footer-add-button:hover {
    background-color: #a6a6a6;
}

        """