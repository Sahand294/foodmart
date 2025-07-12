import psycopg2
import psycopg2.extras
class Cots:
    def __init__(self):

        self.connection = psycopg2.connect(host='127.0.0.1',database='foodmart',port=5432,user='postgres',password='sahand91')
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)