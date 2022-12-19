DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    description TEXT,
    status INTEGER NOT NULL
);

INSERT INTO tasks (title, date, description, status) VALUES
("Lavar a louça", "26/01/1998", "Risco de acidente", 0),
("Tratar as cadelas", "", "Vamos viajar", 0);