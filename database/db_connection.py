import mysql.connector

def get_connection():
    return mysql.connector.connect(user='root',
                                   password='secret',
                                   host='127.0.0.1',
                                   database='library_db')