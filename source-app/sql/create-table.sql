USE YourDatabaseName; -- Specify your database name

-- Create Products table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT
);

-- Create Sales table
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT,
    SaleDate DATETIME,
    Quantity INT,
    TotalPrice DECIMAL(10, 2),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE hive.demo.sales(
    _airbyte_ab_id varchar, 
    _airbyte_emitted_at varchar,
    _airbyte_data varchar
    )
WITH (
  external_location = 's3a://demo/data/Sales/',
  format = 'CSV');