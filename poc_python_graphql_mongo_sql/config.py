import os
from sqlalchemy.engine.url import URL


class MongoConfig:
    DEBUG = True
    MONGO_CON_STRING = dict(
        alias="default",
        db=os.environ.get("MONGO_DB"),
        host=os.environ.get("MONGO_SERVER"),
        port=int(os.environ["MONGO_PORT"]),
        username=os.environ.get("MONGO_USER_NAME"),
        password=os.environ.get("MONGO_PASSWORD"),
        authentication_source="default",
    )


class SQLConfig:
    DEBUG = True
    SQLALCHEMY_CON_STRING = (
        "mssql+pyodbc://"
        + os.environ["USER"]
        + ":"
        + os.environ["PASSWORD"]
        + "@"
        + "MYMSSQL"
    )
