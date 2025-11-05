import psycopg2
from psycopg2 import pool
import sys

class DatabaseConnection:
    """Clase para gestionar la conexión a PostgreSQL"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, minconn=1, maxconn=10):
        """Inicializa el pool de conexiones"""
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host="localhost",
                database="mercado_db",
                user="postgres",
                password="25250101",  # CAMBIAR ESTO
                port="5432"
            )
            print("✓ Pool de conexiones creado exitosamente")
            return True
        except psycopg2.Error as e:
            print(f"✗ Error al crear pool de conexiones: {e}")
            return False
    
    @classmethod
    def get_connection(cls):
        """Obtiene una conexión del pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        
        try:
            connection = cls._connection_pool.getconn()
            return connection
        except psycopg2.Error as e:
            print(f"✗ Error al obtener conexión: {e}")
            return None
    
    @classmethod
    def return_connection(cls, connection):
        """Devuelve una conexión al pool"""
        if cls._connection_pool and connection:
            cls._connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        """Cierra todas las conexiones del pool"""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            print("✓ Todas las conexiones cerradas")
    
    @classmethod
    def test_connection(cls):
        """Prueba la conexión a la base de datos"""
        conn = cls.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✓ Conexión exitosa a PostgreSQL")
                print(f"  Versión: {version[0][:50]}...")
                cursor.close()
                cls.return_connection(conn)
                return True
            except psycopg2.Error as e:
                print(f"✗ Error en test de conexión: {e}")
                if conn:
                    cls.return_connection(conn)
                return False
        return False


# Función auxiliar para ejecutar consultas
def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una consulta SQL
    
    Args:
        query (str): Consulta SQL
        params (tuple): Parámetros de la consulta
        fetch (bool): Si True, retorna los resultados
    
    Returns:
        list/bool: Resultados si fetch=True, sino True/False según éxito
    """
    conn = DatabaseConnection.get_connection()
    if not conn:
        return False if not fetch else []
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch:
            results = cursor.fetchall()
            cursor.close()
            DatabaseConnection.return_connection(conn)
            return results
        else:
            conn.commit()
            cursor.close()
            DatabaseConnection.return_connection(conn)
            return True
            
    except psycopg2.Error as e:
        print(f"✗ Error en consulta: {e}")
        if conn:
            conn.rollback()
            DatabaseConnection.return_connection(conn)
        return False if not fetch else []