from prostgresssql.connection_curser import Cots
class Create:
    def __init__(self,table_name,keys):
        c = Cots()
        connection = c.connection
        cursor = c.cursor
        cursor.execute(f"CREATE TABLE {table_name}({keys})")
        connection.commit()
        connection.close()
        print('Successfully created')