from pyodbc import connect
from faker import Faker

from random import randint, uniform
from argparse import ArgumentParser
from time import sleep

# Connection settings
server = 'mssql'
database = 'demo'
username = 'sa'
password = 'adiosplofe12@@'
driver = 'ODBC Driver 17 for SQL Server'

url = f'DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}'

# Establish connection
conn = connect(url)


# Function to insert records into Sales table
def insert_into_sales(product_id, sale_date, quantity, total_price):
    cursor = conn.cursor()
    sql = "INSERT INTO Sales (ProductID, SaleDate, Quantity, TotalPrice) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (product_id, sale_date, quantity, total_price))
    conn.commit()
    cursor.close()

# Function to retrieve a random product ID from Products table
def get_random_product():
    random_id = randint(1, 5)
    cursor = conn.cursor()
    cursor.execute(f"SELECT ProductID, UnitPrice FROM Products WHERE ProductId = {random_id}")
    row = cursor.fetchone()
    product_id, unit_price = row[0], row[1] if row else None
    cursor.close()
    return {
        "product_id": product_id,
        "unit_price": unit_price
    }

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--batch-size", type=int, help="Number of rows to insert in each batch.", required=True)
    args = parser.parse_args() 

    batch_size: int = args.batch_size
    fake = Faker()

    while True:
        try:
            for loop in range(batch_size):
                product = get_random_product()
                if product:
                    sale_date = fake.date_time_between(start_date='-1y', end_date='now')
                    quantity = randint(1, 10)
                    insert_into_sales(
                        product_id=product.get("product_id"),
                        sale_date=sale_date,
                        quantity=quantity,
                        total_price=product.get("unit_price") * quantity
                    )
            sleep(1)
            print(f"{batch_size} records were inserted!")
        except KeyboardInterrupt:
            conn.close()
