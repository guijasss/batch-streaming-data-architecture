from os import environ
from argparse import ArgumentParser
from datetime import datetime

from polars import col, scan_ndjson
from polars.datatypes import Datetime
from dotenv import load_dotenv

from helpers import camel_to_snake, get_milestone

load_dotenv()

parser = ArgumentParser(description="Moves data from Staging layer to Bronze layer.")
parser.add_argument("-t", "--table", type=str, help="Staging table name", required=True)
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

bronze_table_milestone: datetime = get_milestone("bronze", bronze_table)
print(f"Milestone for table bronze.{bronze_table}: {bronze_table_milestone}")

df = (scan_ndjson(f"s3://delta-lake/layers/staging/{staging_table}/", storage_options=storage_options)
        .unnest("_airbyte_data")
        .cast({"_ab_cdc_deleted_at": Datetime, "_ab_cdc_updated_at": Datetime})
        .filter(col("_ab_cdc_updated_at") > bronze_table_milestone)
        .collect()
    )

print(df.shape)

table_path = f"s3://delta-lake/layers/bronze/{bronze_table}/"

(df
    .write_delta(table_path,
        mode="merge",
        delta_write_options={
            "schema_mode": "overwrite"
        },
        storage_options={
            "AWS_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
            "AWS_REGION": "us-east-1",
            "AWS_ENDPOINT_URL": "http://localhost:9000",
            "AWS_ALLOW_HTTP": "true",
            "AWS_S3_ALLOW_UNSAFE_RENAME": "true"
        },
        delta_merge_options={
            "predicate": "source.order_id = target.order_id",
            "source_alias": "source",
            "target_alias": "target"
        }
    )
    .when_matched_update_all()
    .when_not_matched_insert_all()
    .when_not_matched_by_source_delete()
    .execute()
)
