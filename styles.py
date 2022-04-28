from PyQt5.QtGui import QFont


fonts = {
    "card-title" : QFont("Helvetica", 12, QFont.Bold),
    "card-date" : QFont("Helvetica", 12, QFont.Bold),
    "card-description" : QFont("Helvetica", 10, QFont.Normal),
    "card-button" : QFont("Helvetica", 12, QFont.Bold),
    "header-title" : QFont("Helvetica", 18, QFont.Bold),
    "close-button" : QFont("Helvetica", 18, QFont.Bold),
}

stylesheet = """
QWidget#Landing {
    background-color: white;
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
    background-color: blue;
}

QWidget#card:pressed {
    background-color: black;
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

QPushButton#close-button {
    background-color: red;
    width: 30px;
    height: 30px;
}

        """