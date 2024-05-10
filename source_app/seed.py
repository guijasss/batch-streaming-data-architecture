import pandas as pd
from source_app.mssql import MSSQLHandler


def insert_data_into_mssql(dataframe_path: str, target_table: str):
    df = pd.read_csv(dataframe_path)
    columns = df.columns.tolist()
    values = df.values.tolist()

    db = MSSQLHandler()
    db.insert(target_table, columns, values)

if __name__ == "__main__":
    insert_data_into_mssql("data/olist_customers_dataset.csv", "Customers")
    insert_data_into_mssql("data/olist_geolocation_dataset.csv", "Geolocation")
    insert_data_into_mssql("data/olist_products_dataset.csv", "Products")
    insert_data_into_mssql("data/olist_sellers_dataset.csv", "Sellers")
