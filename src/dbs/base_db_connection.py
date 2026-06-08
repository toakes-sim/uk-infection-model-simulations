import mysql.connector
import uuid
import os

class BaseDBConnection():
    def __init__(self):
        self.connector = mysql.connector
        self.cnx =self.connector.connect(
            user=os.environ['MYSQLUSERNAME'],
            password=os.environ['MYSQLPASSWORD'],
            host='localhost',
            database=os.environ['MYSQLDATABASENAME'])
        self.cursor = self.cnx.cursor(dictionary=True)

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def close(self):
        self.cnx.close()
