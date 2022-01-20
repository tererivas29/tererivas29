import pyodbc
import pandas as pd
import os

# CONS
_TABLE_NAMES = (
    "table1",
    "table2",
    "table3",
    "table4",
    "table5",
)
_SCHEMA_NAMES = ["dbo"]

# SET ENV VARIABLES
db_server = os.environ.get("SERVER")
db_name = "TEST_DB"
db_user_name = str(os.environ.get("USER"))
db_user_password = os.environ.get("PASSWORD")


# connects to an SQL server and executes a query, with the params specified.
def sql_db_connect_and_execute(query, params):
    try:
        my_db_connection = pyodbc.connect(
            SERVER=db_server,
            applicationintent="readonly",
            DATABASE=db_name,
            PORT=1433,
            USER=db_user_name,
            PASSWORD=db_user_password,
            DRIVER="FreeTDS",
        )
        print("Connection to DB successful")

        df = pd.DataFrame(
            pd.read_sql(query, my_db_connection, params=params, index_col="TableName"),
        )

        print("*******df ")
        print(df)

        my_db_connection.close()

        return df

        # execute query and return df
    except Exception as e:
        print(str(e))


# query to get the size of a list of tables
def query_tables():
    # form query with params
    # timestamp format is yyyy-mm-dd hh:mm:ss
    query = f"""SELECT t.NAME AS TableName,
        p.rows AS RowCounts,
        s.Name AS SchemaName,
        convert(varchar, getdate(), 120) AS TimeStamp,
        CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS SizeInMB
FROM
    sys.tables t
INNER JOIN
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN
    sys.partitions p ON i.object_id = p.OBJECT_ID
    AND i.index_id = p.index_id
INNER JOIN
    sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN
    sys.schemas s ON t.schema_id = s.schema_id
WHERE t.NAME in ({','.join(['?']*len(_TABLE_NAMES))}) 
AND t.is_ms_shipped = 0
AND i.OBJECT_ID > 255
GROUP BY t.Name, s.Name, p.rows
ORDER BY SizeInMB DESC, t.Name"""

    return sql_db_connect_and_execute(query, _TABLE_NAMES)


# query to get the size of an schema
def query_schema():
    # form query with params
    # timestamp format is yyyy-mm-dd hh:mm:ss
    schema_size_query = f"""SELECT SCHEMA_NAME(so.schema_id) AS SchemaName,
    convert(varchar, getdate(), 120) AS TimeStamp,
    CAST(ROUND(((SUM(ps.reserved_page_count) * 8.0) / 1024), 2) AS NUMERIC(36, 2)) AS SizeInMB
    FROM sys.dm_db_partition_stats ps
    JOIN sys.indexes i ON i.object_id = ps.object_id
    AND i.index_id = ps.index_id
    JOIN	sys.objects	so
    ON	i.object_id =	so.object_id
    WHERE so.type = 'U'
    AND SCHEMA_NAME(so.schema_id) in ({','.join(['?']*len(_SCHEMA_NAMES))}) 
    GROUP BY	so.schema_id
    """

    return sql_db_connect_and_execute(schema_size_query, _SCHEMA_NAMES)
