from config import MongoConfig, SQLConfig

from mongoengine import connect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker

# Mongo DB Connection conf
mongo_db_session = connect(**MongoConfig.MONGO_CON_STRING)

# SQL DB connection conf
engine = create_engine(
    SQLConfig.SQLALCHEMY_CON_STRING,
    echo=True,
)

sql_db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base(cls=DeferredReflection)
Base.query = sql_db_session.query_property()
