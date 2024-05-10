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
    CREATE DATABASE demo;

    USE demo;

    CREATE TABLE Users (
        id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
        first_name VARCHAR(MAX) NOT NULL,
        last_name VARCHAR(MAX) NOT NULL,
        email VARCHAR(MAX) NOT NULL,
        password VARCHAR(MAX) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Products (
        id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(MAX) NOT NULL,
        sku VARCHAR(MAX),
        price FLOAT,
        units_in_stock SMALLINT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Purchases (
        id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
        user_id INT FOREIGN KEY REFERENCES Users(id),
        product_id INT FOREIGN KEY REFERENCES Products(id),
        purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Ratings (
        id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
        user_id INT FOREIGN KEY REFERENCES Users(id),
        product_id INT FOREIGN KEY REFERENCES Products(id),
        stars INT NOT NULL,
        comment VARCHAR(MAX)
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

    EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name   = 'Products',
    @role_name     = 'adm',
    @supports_net_changes = 0

    EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name   = 'Users',
    @role_name     = 'adm',
    @supports_net_changes = 0

    EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name   = 'Purchases',
    @role_name     = 'adm',
    @supports_net_changes = 0

    EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name   = 'Reviews',
    @role_name     = 'adm',
    @supports_net_changes = 0
    ```

