from typing import List

from pyodbc import connect, Cursor, Connection

class MSSQLHandler():
    def __init__(self) -> None:
        self.server = '172.21.0.13'
        self.database = 'demo'
        self.username = 'sa'
        self.password = 'adiosplofe12@@'
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.url = (
            f'DRIVER={{{self.driver}}};'
            f'SERVER={self.server},1433;'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'Connection Timeout=90;'  # Set timeout to 30 seconds
        )
        self.connection: Connection = connect(self.url)

    def insert(self, table_name: str, columns: List[str], values: List[list]):
        cursor: Cursor = self.connection.cursor()
        cursor.fast_executemany = True
        values_placeholder = "(" + ", ".join(["?"] * len(columns)) + ")"
        sql = f"INSERT INTO demo.dbo.{table_name} ({', '.join(columns)}) VALUES {values_placeholder}"

        cursor.executemany(sql, values)
        self.connection.commit()
        cursor.close()
