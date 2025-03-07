from json import loads
from typing import TypedDict

from pandas import read_csv

from repositories import Repository, PostgresRepository
from entities import Item, Order, Payment, Review


class OrderData(TypedDict):
    order: dict
    review: dict
    items: list
    payment: dict


class BatchDataProducer:
    def __init__(self, repository: Repository):
        self.repository = repository

    def generate_order(self) -> OrderData:
        data_dir = "./data/ecommerce-data"

        orders = read_csv(f"{data_dir}/olist_orders_dataset.csv")
        orders_batch = orders.sample(1)

        orders_indexes = orders_batch["order_id"].values.tolist()

        order_reviews = read_csv(f"{data_dir}/olist_order_reviews_dataset.csv")
        order_payments = read_csv(f"{data_dir}/olist_order_payments_dataset.csv")
        order_items = read_csv(f"{data_dir}/olist_order_items_dataset.csv")

        reviews_batch = order_reviews[order_reviews["order_id"].isin(orders_indexes)]
        payments_batch = order_payments[order_payments["order_id"].isin(orders_indexes)]
        items_batch = order_items[order_items["order_id"].isin(orders_indexes)]

        return {
            "order": loads(orders_batch.to_json(orient="records"))[0],
            "review": loads(reviews_batch.to_json(orient="records"))[0],
            "payment": loads(payments_batch.to_json(orient="records"))[0],
            "items": loads(items_batch.to_json(orient="records"))
        }

    def execute(self):
        return self.generate_order()

host = "localhost"
database = "postgres"
username = "postgres"
password = "example"

repo = PostgresRepository(host, database, username, password)
producer = BatchDataProducer(repo)
order_data: dict = producer.generate_order()

repo.insert_from_json(Order, order_data['order'])

for item in order_data['items']:
    repo.insert_from_json(Item, item)

repo.insert_from_json(Payment, order_data['payment'])

if order_data['review']:
    repo.insert_from_json(Review, order_data['review'])
