from abc import ABC
from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from entities import Item, Order, Payment, Review


class Repository(ABC):
    def __init__(self, host: str, database: str, username: str, password: str, port: int):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    def insert(self, table_name: str, columns: List[str], values: List[List[Any]]):
        raise NotImplementedError("Implement this method in subclasses!")
    

class PostgresRepository(Repository):
    def __init__(self, host, database, username, password, port=5432):
        super().__init__(host, database, username, password, port)
        DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

        self.engine = create_engine(DATABASE_URL)
        self.session = sessionmaker(bind=self.engine)()
        self._create_tables()

    def _create_tables(self):
        Base = declarative_base()
        Base.metadata.create_all(self.engine)

    def insert_from_json(self, Model: Any, data: dict) -> None:
        new_data = Model(**data)
        self.session.add(new_data)
        self.session.commit()

    def insert(self, table_name, columns, values) -> None:
        return super().insert(table_name, columns, values)
    