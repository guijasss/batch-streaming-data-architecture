# About
## Data Pipeline Architecture
![Architecture](/docs/architecture.png)

# Setup

* Start services
    ```sh
    docker-compose up -d
    ```

* Start Airbyte
    ```sh
    git clone --depth=1 https://github.com/airbytehq/airbyte.git
    ./airbyte/run-ab-platform.sh
    ```

* Create a new database
    ```sql
    -- CDC don't work with default database 'master', so we need to create another one.
    CREATE DATABASE demo;
    ```

* Enable SQL Server Agent
    * SQL Server Agent should be enabled inside SQL Server container. To access container, you can run:
    ```sh
    docker exec -it mssql bash
    ```

    * Inside container, enable SQL Server Agent.
    ```sh
    sudo /opt/mssql/bin/mssql-conf set sqlagent.enabled true
    ```

    * After that, restart service.
    ```sh
    docker-compose restart
    ```

* Create transactional databases
    ```sql
    USE demo;

    CREATE TABLE Products (
        ProductID INT PRIMARY KEY,
        ProductName NVARCHAR(100),
        UnitPrice DECIMAL(10, 2),
        UnitsInStock INT
    );

    CREATE TABLE Sales (
        SaleID INT PRIMARY KEY IDENTITY(1,1),
        ProductID INT,
        SaleDate DATETIME,
        Quantity INT,
        TotalPrice DECIMAL(10, 2),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    );
    ```

* Enable CDC
    * To enable CDC, a SQL Server administrator with the necessary privileges (db_owner or sysadmin) must first run a query to enable CDC at the database level.

    ```sql
    USE demo
    GO
    EXEC sys.sp_cdc_enable_db
    GO
    ```

    * The administrator must then enable CDC for each table that you want to capture. Here's an example:

    ```sql
    USE demo
    GO

    EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name   = 'Sales',
    @role_name     = 'adm',
    @supports_net_changes = 0
    GO
    ```

