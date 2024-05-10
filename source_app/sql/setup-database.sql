CREATE DATABASE demo;

USE demo;

CREATE TABLE Customers (
	customer_id VARCHAR(MAX),
	customer_unique_id VARCHAR(MAX),
	customer_zip_code_prefix VARCHAR(5),
	customer_city VARCHAR(MAX),
	customer_state VARCHAR(2)
);

CREATE TABLE Geolocation (
	geolocation_zip_code_prefix VARCHAR(5),
	geolocation_lat FLOAT,
	geolocation_lng FLOAT,
	geolocation_city VARCHAR(MAX),
	geolocation_state VARCHAR(2)
);

CREATE TABLE OrderItems (
	order_id VARCHAR(MAX),
	order_item_id TINYINT,
	product_id VARCHAR(MAX),
	seller_id VARCHAR(MAX),
	shipping_limit_date DATETIME,
	price FLOAT,
	freight_value FLOAT
);

CREATE TABLE OrderPayments (
	order_id VARCHAR(MAX),
	payment_sequential TINYINT,
	payment_type VARCHAR(MAX),
	payment_installments VARCHAR(MAX),
	payment_value FLOAT
)

CREATE TABLE OrderReviews (
	review_id VARCHAR(MAX),
	order_id VARCHAR(MAX),
	review_score SMALLINT,
	review_comment_title VARCHAR(MAX),
	review_comment_message VARCHAR(MAX),
	review_creation_date DATETIME,
	review_answer_timestamp DATETIME
)

CREATE TABLE Orders (
	order_id VARCHAR(MAX),
	customer_id VARCHAR(MAX),
	order_status VARCHAR(MAX),
	order_purchase_timestamp DATETIME2,
	order_approved_at DATETIME2,
	order_delivered_carrier_date DATETIME2,
	order_delivered_customer_date DATETIME2,
	order_estimated_delivery_date DATETIME2
)

CREATE TABLE Products (
	product_id VARCHAR(MAX),
	product_category_name VARCHAR(MAX),
	product_name_lenght FLOAT,
	product_description_lenght FLOAT,
	product_photos_qty FLOAT,
	product_weight_g FLOAT,
	product_length_cm FLOAT,
	product_height_cm FLOAT,
	product_width_cm FLOAT
)

CREATE TABLE Sellers (
	seller_id VARCHAR(MAX),
	seller_zip_code_prefix VARCHAR(5),
	seller_city VARCHAR(MAX),
	seller_state VARCHAR(2)
)
