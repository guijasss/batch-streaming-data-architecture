from pyodbc import connect, Cursor, Connection
from faker import Faker

from numpy import arange
from random import choice
from argparse import ArgumentParser
from time import sleep


class DatabaseFaker():
    def __init__(self) -> None:
        self.server = 'localhost'
        self.database = 'demo'
        self.username = 'sa'
        self.password = 'adiosplofe12@@'
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.url = f'DRIVER={{{self.driver}}};SERVER={self.server},1433;DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.connection: Connection = connect(self.url)
        self.faker = Faker()

    def get_random_id(self, table: str) -> int:
        cursor: Cursor = self.connection.cursor()
        sql = f"SELECT TOP 1 id FROM demo.dbo.{table.title()} ORDER BY NEWID()"
        random_id: int = cursor.execute(sql).fetchone()[0]
        cursor.close()
        return random_id
    
    def generate_purchase(self, verbose: bool):
        cursor: Cursor = self.connection.cursor()
        user_id: int = self.get_random_id("Users")
        product_id: int = self.get_random_id("Products")
        sql = "INSERT INTO demo.dbo.Purchases (user_id, product_id) VALUES (?, ?)"
        cursor.execute(sql, (user_id, product_id))

        if verbose:
            print({
                "user_id": user_id,
                "product_id": product_id
            })

        self.connection.commit()
        cursor.close()

    def generate_rating(self, verbose: bool):
        cursor: Cursor = self.connection.cursor()
        purchase_id: int = self.get_random_id("Purchases")
        purchases_sql_select = f"SELECT user_id, product_id FROM demo.dbo.Purchases WHERE id = {purchase_id}"
        cursor.execute(purchases_sql_select)
        
        user_id, product_id = cursor.fetchone()
        stars = choice(arange(0, 5.1, 0.5).tolist())
        comment = self.faker.paragraph()
        ratings_insert_sql = f"INSERT INTO demo.dbo.Ratings (user_id, product_id, stars, comment) VALUES (?, ?, ?, ?)"
        cursor.execute(ratings_insert_sql, (user_id, product_id, stars, comment))

        if verbose:
            print({
                "user_id": user_id,
                "product_id": product_id,
                "stars": stars,
                "comment": comment
            })

        self.connection.commit()
        cursor.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--table", help="Table to insert data", type=str)
    parser.add_argument("--batch-size", help="How many rows to insert in table", type=int)
    parser.add_argument("--verbose", "-v", help="Whether to print inserted data", const=True, nargs="?")
    args = parser.parse_args()

    table = args.table
    batch_size = args.batch_size
    verbose = args.verbose is not None

    db_faker = DatabaseFaker()

    table_to_insert_function_mapping = {
        "purchases": db_faker.generate_purchase,
        "ratings": db_faker.generate_rating
    }

    for _ in range(batch_size):
        table_to_insert_function_mapping.get(table)(verbose)
    