from pyodbc import connect
from faker import Faker

from random import randint, uniform

# Connection settings
server = 'mssql'
database = 'demo'
username = 'sa'
password = 'adiosplofe12@@'
driver = 'ODBC Driver 17 for SQL Server'

url = f'DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}'

# Establish connection
print(url)
conn = connect(url)


# Function to insert records into Sales table
def insert_into_sales(product_id, sale_date, quantity, total_price):
    cursor = conn.cursor()
    print(f"Sale(product_id={product_id},sale_date={sale_date},quantity={quantity},total_price={total_price})")
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
    fake = Faker()
    loops = 50

    for loop in range(loops):
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
            print("Sale inserted successfully.")
        else:
            print("No products found in the Products table.")

    # Close connection
    conn.close()
