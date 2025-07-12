from prostgresssql.connection_curser import Cots

class Update:
    def __init__(self,table:str,column:str,new_value:str,condition:str):
        c = Cots()
        co = c.connection
        cu = c.cursor
        cu.execute(f"UPDATE {table} SET {column} = {new_value}  WHERE {condition};")
        co.commit()
        co.close()
        print('Successfully updated')
