from argparse import ArgumentParser
from datetime import datetime

from pandas import isnull, read_csv

from mssql import MSSQLHandler


def parse_timestamp(date_str):
    if date_str is None or isnull(date_str):
        return None
    else:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    

def generate_order_data(batch_size: int) -> None:
    data_dir = "notebooks/data/ecommerce-data"

    orders = read_csv(f"{data_dir}/olist_orders_dataset.csv")
    orders_batch = orders.sample(batch_size)
    orders_batch["order_purchase_timestamp"] = orders_batch["order_purchase_timestamp"].apply(parse_timestamp)
    orders_batch["order_approved_at"] = orders_batch["order_approved_at"].apply(parse_timestamp)
    orders_batch["order_delivered_carrier_date"] = orders_batch["order_delivered_carrier_date"].apply(parse_timestamp)
    orders_batch["order_delivered_customer_date"] = orders_batch["order_delivered_customer_date"].apply(parse_timestamp)
    orders_batch["order_estimated_delivery_date"] = orders_batch["order_estimated_delivery_date"].apply(parse_timestamp)

    orders_indexes = orders_batch["order_id"].values.tolist()

    order_reviews = read_csv(f"{data_dir}/olist_order_reviews_dataset.csv")
    order_payments = read_csv(f"{data_dir}/olist_order_payments_dataset.csv")
    order_items = read_csv(f"{data_dir}/olist_order_items_dataset.csv")

    reviews_batch = order_reviews[order_reviews["order_id"].isin(orders_indexes)]
    payments_batch = order_payments[order_payments["order_id"].isin(orders_indexes)]
    items_batch = order_items[order_items["order_id"].isin(orders_indexes)]

    db = MSSQLHandler()
    db.insert("Orders", orders_batch.columns, orders_batch.values.tolist())
    db.insert("OrderReviews", reviews_batch.columns, reviews_batch.values.tolist())
    db.insert("OrderItems", items_batch.columns, items_batch.values.tolist())
    db.insert("OrderPayments", payments_batch.columns, payments_batch.values.tolist())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--batch-size", help="How many rows to insert in table", type=int)
    args = parser.parse_args()

    batch_size = args.batch_size

    generate_order_data(batch_size)
    print(f"Inserted {batch_size} rows successfully!")
