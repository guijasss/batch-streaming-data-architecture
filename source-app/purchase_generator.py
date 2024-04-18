from pyodbc import connect
from faker import Faker

from random import randint, uniform
from argparse import ArgumentParser
from time import sleep

# Connection settings
server = 'localhost'
database = 'demo'
username = 'sa'
password = 'adiosplofe12@@'
driver = 'ODBC Driver 17 for SQL Server'

url = f'DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}'

# Establish connection
conn = connect(url)

# Function to insert records into Sales table
def insert_into_purchases():
    cursor = conn.cursor()
    user_id = randint(1, 4)
    product_id = randint(1, 5)
    sql = "INSERT INTO Purchases (user_id, product_id) VALUES (?, ?)"
    cursor.execute(sql, (user_id, product_id))
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--batch-size", type=int, help="Number of rows to insert in each batch.", required=True)
    args = parser.parse_args() 

    batch_size: int = args.batch_size
    fake = Faker()

    for loop in range(batch_size):
        insert_into_purchases()
    
    print(f"{batch_size} records were inserted!")
    conn.close()
