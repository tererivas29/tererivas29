from sqlalchemy import Column, Integer

from mongoengine import DynamicDocument
from mongoengine.fields import (
    IntField,
    StringField,
)
from sqlalchemy.sql.sqltypes import String
from database import Base, engine

# collections conf for Mongo
class DriverMongoModel(DynamicDocument):

    meta = {"collection": "mongoCollectionName"}
    driverId = IntField(required=False)
    field1 = StringField(required=False)
    field2 = StringField(required=False)
    Field3 = IntField(required=False)


# tables conf for SQL
class DriverSQLModel(Base):  # type: ignore
    __tablename__ = "slqTableName"
    driverId = Column(String, primary_key=True)
    field1 = Column(String)
    field2 = Column(String)
    field3 = Column(String)
    field4 = Column(String)
    __table_args__ = {"schema": "dbo"}

Base.prepare(engine)
