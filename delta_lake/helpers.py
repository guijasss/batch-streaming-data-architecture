from re import sub
from datetime import datetime
from os import environ

from polars import read_delta
from deltalake.exceptions import TableNotFoundError

def camel_to_snake(camel_str: str) -> str:
    return sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def get_milestone(layer: str, table: str) -> datetime:
    MINIO_ACCESS_KEY_ID = environ["MINIO_ACCESS_KEY_ID"]
    MINIO_SECRET_ACCESS_KEY = environ["MINIO_SECRET_ACCESS_KEY"]
    storage_options={
        "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
        "AWS_REGION": "us-east-1",
        "AWS_ENDPOINT_URL": "http://localhost:9000",
        "AWS_ALLOW_HTTP": "true",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true"
    }

    try:
        milestone: str = (read_delta(f"s3://delta-lake/layers/{layer}/{table}/",
                storage_options=storage_options,
                columns=["_ab_cdc_updated_at"]
            )             
            .max()
            .select("_ab_cdc_updated_at")
            .row(0)[0]
        ) or datetime(2019, 1, 1)

        return milestone  #'%Y-%m-%dT%H:%M:%S')
    
    except TableNotFoundError:
        return datetime(2019, 1, 1)
