import pandas as pd
import pyodbc
import os

# SET ENV VARIABLES
db_server = os.environ.get("_SERVER_NAME")
db_name = os.environ.get("_DATA_BASE_NAME")
db_user_name = os.environ.get("_DB_USER_NAME")
db_user_password = os.environ.get("_DB_PASSWORD")

# in this case specify all necessary TDS parameters.
conn = pyodbc.connect(
    SERVER=db_server,
    DATABASE=db_name,
    PORT=1433,
    USER=db_user_name,
    PASSWORD=db_user_password,
    DRIVER="FreeTDS",
)
cursor = conn.cursor()
print("Connection to MySQL DB successful")


# function to execute query
def read(self):
    print("read")
    #here you put the query you want to execute
    data = pd.read_sql("select top(10) * from table", conn)
    ordered = data.sort_values("table_id", ascending=False)
    get_column = data.get("table_id")
    specific_driver = data.at[0, "table_id"]

    print(ordered)
    print(get_column)
    print(specific_driver)


read(conn)  # call the funtion

conn.close()  # method to close open connections after work is completed.
