import sqlite3
import os
import threading


class Database:
    def __init__(self):
        self.db_name = 'student_management.db'
        self.local = threading.local()
        self.create_tables()

    def get_conenction(self):
        """Keeping exact method name as in original"""
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.local.cursor = self.local.connection.cursor()
        return self.local.connection, self.local.cursor

    def create_tables(self):
        con = sqlite3.connect(self.db_name, check_same_thread=False)
        cur = con.cursor()

        # Create courses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                cid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                duration TEXT,
                charges TEXT,
                description TEXT
            )
        ''')

        # Create students table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                gender TEXT,
                dob TEXT,
                contact TEXT,
                admission TEXT,
                course TEXT,
                state TEXT,
                city TEXT,
                pin TEXT,
                address TEXT
            )
        ''')

        # Create results table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS results (
                rid INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,
                name TEXT,
                course TEXT,
                marks TEXT,
                total_marks TEXT,
                percentage TEXT
            )
        ''')

        con.commit()
        con.close()