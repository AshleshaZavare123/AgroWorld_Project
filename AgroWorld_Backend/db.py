import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="gauri413736#",
        database="agroworld"
    )
