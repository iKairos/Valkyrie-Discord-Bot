import sqlite3 as sql

class DB_Helpers():
    """
    Class of helper functions that will help us to interact with the database.
    """
    def __init__(self, db_directory):
        self.db_directory = db_directory
        
    def connect(self):
        try:
            conn = sql.connect(self.db_directory)
            return conn
        except Exception as e:
            print(e)
        
        return None

    def spawn_table(self, string):
        try:
            c = self.connect().cursor()
            c.execute(string)
        except Exception as e:
            print(e)
    
    def do_operation(self, operation, input_values):
        uplink = self.connect()
        c = uplink.cursor()
        c.execute(operation, input_values)
        uplink.commit()
    
    def append_row(self, table, **kwargs):
        cols = [x for x in kwargs]
        equated = tuple([kwargs[x] for x in kwargs])
        runner = "INSERT INTO {}(" + "{}, " * len(kwargs) + ") "
        runner = runner + "VALUES (" + "?, " * len(kwargs) + ")"
        runner = runner.format(table, *cols)
        runner = runner.replace(', )', ')') 
        
        equated = tuple([kwargs[x] for x in kwargs])

        try:
            self.do_operation(runner, equated)
        except Exception as e:
            print(e)
    
    def purge_row(self, table, **kwargs):
        cols = [x for x in kwargs]
        runner = "DELETE FROM {} WHERE " + "{} = ? AND " * len(kwargs) + "!@#"
        runner = runner.format(table, *cols)
        runner = runner.replace("AND !@#", "")

        equated = tuple([kwargs[x] for x in kwargs])

        try:
            self.do_operation(runner, equated)
        except Exception as e:
            print(e)
    
    def fetch_row(self, table, **kwargs):
        if len(kwargs) == 0:
            runner = f"SELECT * FROM {table}"
            uplink = self.connect()
            c = uplink.cursor()
            c.execute(runner, ())
            fetched = c.fetchall()
            return fetched
        
        cols = [x for x in kwargs]
        equated = tuple([kwargs[x] for x in kwargs])
        runner = "SELECT * FROM {} WHERE " + "{} = ? AND " * len(kwargs) + "!@#"
        runner = runner.format(table, *cols)
        runner = runner.replace("AND !@#", "")

        uplink = self.connect()
        c = uplink.cursor()
        c.execute(runner, equated)
        fetched = c.fetchall()
        return fetched
    
    def update_data(self, table, column, new_value, **kwargs):
        cols = [x for x in kwargs]
        equated = tuple([new_value] + [kwargs[x] for x in kwargs])
        runner = "UPDATE {} SET {} = ? WHERE ".format(table, column)
        runner = runner + "{} = ? AND " * len(kwargs)
        runner = runner + "!@#"
        runner = runner.replace("AND !@#", "")
        runner = runner.format(*cols)

        try:
            self.do_operation(runner, equated)
        except Exception as e:
            print(e)
    



    

    
    


