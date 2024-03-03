# Setup
```sh
docker-compose up -d
./run-ab-platform.sh
```

# Setup SQL Server

* Create a new database

CDC don't work with default database 'master', so we need to create another one.
```sql
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

