import mysql.connector

def conectar():
    """
    Devuelve una conexión activa a la base de datos TallerMecanico.
    """
    return mysql.connector.connect(
        host="localhost",
        user="dios",
        password="pass123",
        database="TallerMecanico"
    )
