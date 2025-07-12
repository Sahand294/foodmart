from prostgresssql.connection_curser import Cots
class Deleting:
    def __init__(self,table):
        c = Cots()
        connection = c.connection
        cursor = c.cursor
        cursor.execute(f'DROP TABLE {table}')
        connection.commit()
        connection.close()
        print('Successfully deleted')