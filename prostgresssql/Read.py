from prostgresssql.connection_curser import  Cots

class Reading:
    @staticmethod
    def read(table):
        c = Cots()
        connection = c.connection
        cursor = c.cursor
        cursor.execute(f'SELECT * FROM {table}')
        c = cursor.fetchall()
        o = []
        for i in c:
            o.append(dict(i))
        return o