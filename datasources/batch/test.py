from datetime import datetime
from json import dumps, loads

from pandas import read_csv, isnull


def parse_timestamp(date_str):
    if date_str is None or isnull(date_str):
        return None
    else:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

data_dir = "./data/ecommerce-data"

orders = read_csv(f"{data_dir}/olist_orders_dataset.csv")
orders_batch = orders.sample(1)
#orders_batch["order_purchase_timestamp"] = orders_batch["order_purchase_timestamp"].apply(parse_timestamp)
#orders_batch["order_approved_at"] = orders_batch["order_approved_at"].apply(parse_timestamp)
#orders_batch["order_delivered_carrier_date"] = orders_batch["order_delivered_carrier_date"].apply(parse_timestamp)
#orders_batch["order_delivered_customer_date"] = orders_batch["order_delivered_customer_date"].apply(parse_timestamp)
#orders_batch["order_estimated_delivery_date"] = orders_batch["order_estimated_delivery_date"].apply(parse_timestamp)

orders_indexes = orders_batch["order_id"].values.tolist()

order_reviews = read_csv(f"{data_dir}/olist_order_reviews_dataset.csv")
order_payments = read_csv(f"{data_dir}/olist_order_payments_dataset.csv")
order_items = read_csv(f"{data_dir}/olist_order_items_dataset.csv")

reviews_batch = order_reviews[order_reviews["order_id"].isin(orders_indexes)]
payments_batch = order_payments[order_payments["order_id"].isin(orders_indexes)]
items_batch = order_items[order_items["order_id"].isin(orders_indexes)]

{
    "order": loads(orders_batch.to_json(orient="records"))[0],
    "review": loads(reviews_batch.to_json(orient="records"))[0],
    "payment": loads(payments_batch.to_json(orient="records"))[0],
    "items": loads(items_batch.to_json(orient="records"))[0]
}

print(dumps({
    "order": loads(orders_batch.to_json(orient="records"))[0],
    "review": loads(reviews_batch.to_json(orient="records"))[0],
    "payment": loads(payments_batch.to_json(orient="records"))[0],
    "items": loads(items_batch.to_json(orient="records"))[0]
}))
