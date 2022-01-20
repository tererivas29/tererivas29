import os
import pandas as pd
from pymongo import MongoClient
from pandas.io import sql
import sql_utils as sqlu
import mongo_utils as mngu

# CONS
_SERVER = str(os.environ.get("MONGO_SERVER"))
_PORT = os.environ.get("MONGO_PORT")
_USER_NAME = os.environ.get("MONGO_USER_NAME")
_PASSWORD = os.environ.get("MONGO_PASSWORD")


def mongo_db_connect():
    connection = f"mongodb+srv://{_USER_NAME}:{_PASSWORD}@{_SERVER}"
    # return connection
    return MongoClient(connection, tls=True, tlsAllowInvalidCertificates=True)


# connects to an specific SQL DB to retrieve information and stores that information in the specified Mongos DB and collection
def get_and_store_info(database, query, collection):

    # get info
    df = pd.DataFrame(query)

    df.reset_index(inplace=True)

    # convert data do a dictionary
    data = df.to_dict("records")
    print("***** records to be inserted *****")
    print(data)

    try:
        # connect to mongo
        client = mngu.mongo_db_connect()
        my_db = client[database]

        # insert jsons into mongo
        collection = my_db[collection]
        collection.insert_many(data)

    except Exception as e:
        print("Exception: ")
        print(str(e))


# reads info from a Mongo DBs collection and returns it in a Pandas DF
def read_statistics(database, collection):

    # read data to verify it was stored correctly

    try:
        # connect to mongo
        client = mngu.mongo_db_connect()
        my_db = client[database]
        collection = my_db[collection]

        return pd.DataFrame(list(collection.find()))

    except Exception as e:
        print(str(e))
