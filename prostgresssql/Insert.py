from prostgresssql.connection_curser import Cots

class Inserting:
    def __init__(self,table:str,keys:str,value:str):
        c = Cots()
        connection = c.connection
        cursor = c.cursor
        con = connection
        cur = cursor
        cur.execute(f"INSERT INTO {table}({keys}) VALUES {value}")
        con.commit()
        con.close()
        print('Successfully inserted')