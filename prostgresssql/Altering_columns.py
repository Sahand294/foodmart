from prostgresssql.connection_curser import Cots
c = Cots()
connection = c.connection
cursor = c.cursor
class Alter:
    @staticmethod
    def rename_column(table:str,column_name:str,new_column_name:str):
        cursor.execute(f'ALTER TABLE {table} RENAME COLUMN {column_name} TO {new_column_name}')
        connection.commit()
        connection.close()
        print('Successfully renamed')

    @staticmethod
    def drop_column(table:str,column:str):
        cursor.execute(f'ALTER TABLE {table} DROP COLUMN {column} ')
        connection.commit()
        connection.close()
        print('Successfully droped')

    @staticmethod
    def add_column(table:str,column_name:str,type:str):
        cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column_name} {type}')
        connection.commit()
        connection.close()
        print('Successfully added')

    @staticmethod
    def change_column_type(table:str,column_name:str,type:str):
        cursor.execute(f'ALTER TABLE {table} ALTER COLUMN {column_name} TYPE {type} USING {column_name}::{type}')
        connection.commit()
        connection.close()
        print('Successfully changed the type')
