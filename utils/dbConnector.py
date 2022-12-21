import sqlite3  

class Connector:

    def __init__(self, path : str, schema : str = "", init : bool = False) -> None:
        self.__config = {
            "path" : path if path else "database.db",
            "schema" : schema,
        }
        self.__connect()
        
        if init:
            self.__init_schema()

    def __connect(self):
        db = sqlite3.connect(
            self.__config["path"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        db.row_factory = self.__make_dicts #or sqlite3.Row
        self.__config["db"] = db
        self.__config["cursor"] = db.cursor()

    def __make_dicts(self, cursor, row):
        return dict((cursor.description[idx][0], value)
            for idx, value in enumerate(row))

    def __init_schema(self):
        try:
            script : str = ""
            with open(self.__config["schema"], mode="r", encoding="utf-8") as f:
                
                while True:
                    line = f.readline()
                    if line:
                        script += line
                    else:
                        break
                    
            print(script)
            self.db.executescript(script)
        except sqlite3.OperationalError as e:
            print(f"\nSQL Schema with error {e.args[0]}")

    def reinit(self):
        self.__init_schema()

    @property
    def db(self) -> sqlite3.Connection:
        if 'db' not in self.__config.keys():
            self.__connect()

        return self.__config["db"]

    @property
    def cursor(self) -> sqlite3.Cursor:
        if "cursor" not in self.__config.keys():
            self.__config["cursor"] = self.db.cursor()
        
        return self.__config["cursor"]

    def close(self, e=None):
        self.db.close()

    def query_commit(self, query : str):
        self.cursor.execute(query)
        self.db.commit()

    def query_one(self, query : str) -> dict:
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def query_all(self, query : str) -> list:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def tasks(self) -> dict:
        query : str = "SELECT * FROM tasks ORDER BY id DESC"
        return self.query_all(query)

    def add_task(self, task : str):
        query = "INSERT INTO tasks (title, date, description, status) VALUES " + task
        print(query)
        self.query_commit(query)

    def update_task(self, task : str):
        task = [i.strip() for i in task.strip("()").split(",")]
        query = f"UPDATE tasks SET title = {task[1]}, date = {task[2]}, description = {task[3]}, status = {int(task[4])} WHERE id = {int(task[0])}"
        print(query)
        self.query_commit(query)

if __name__ == "__main__":
    conn = Connector(path="deletar.db", schema="schema.sql", init=True)
