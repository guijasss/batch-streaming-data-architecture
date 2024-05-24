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
    - Run __../source_app/sql/setup-database.sql__ file.

* Enable CDC
    * To enable CDC, a SQL Server administrator with the necessary privileges (db_owner or sysadmin) must first run a query to enable CDC at the database level. After, you must then enable CDC for each table that you want to capture.

    - run __../source_app/sql/enable-cdc.sql__ file.