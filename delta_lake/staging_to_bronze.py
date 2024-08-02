from os import environ
from argparse import ArgumentParser

from polars import scan_ndjson
from polars.datatypes import Datetime
from dotenv import load_dotenv

from delta_lake.helpers import camel_to_snake

load_dotenv()

parser = ArgumentParser(description="Moves data from Staging layer to Bronze layer.")
parser.add_argument("-t", "--table", type=str, help="Staging table name")
args = parser.parse_args()

staging_table: str = args.table
bronze_table: str = camel_to_snake(staging_table)

MINIO_ACCESS_KEY_ID = environ["MINIO_ACCESS_KEY_ID"]
MINIO_SECRET_ACCESS_KEY = environ["MINIO_SECRET_ACCESS_KEY"]

storage_options = {
    "access_key_id": MINIO_ACCESS_KEY_ID,
    "secret_access_key": MINIO_SECRET_ACCESS_KEY,
    "endpoint": "http://localhost:9000"
}

df = (scan_ndjson(f"s3://delta-lake/layers/staging/{staging_table}/", storage_options=storage_options)
      .unnest("_airbyte_data")
      .cast({"_ab_cdc_deleted_at": Datetime})
      .collect()
      )

table_path = f"s3://delta-lake/layers/bronze/{bronze_table}/"


df.write_delta(table_path, mode="overwrite", delta_write_options={
    "schema_mode": "overwrite"
}, storage_options={
        "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
        "AWS_REGION": "us-east-1",
        "AWS_ENDPOINT_URL": "http://localhost:9000",
        "AWS_ALLOW_HTTP": "true",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true"
})
