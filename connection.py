import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("[OK] Terhubung ke database.")
                return True
        except Error as e:
            print(f"[ERROR] Gagal koneksi database: {e}")
        return False

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("[INFO] Koneksi database ditutup.")
