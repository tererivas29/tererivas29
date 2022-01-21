from graphene_sqlalchemy import SQLAlchemyObjectType
from graphhql.models import DriverSQLModel, DriverMongoModel
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from graphene.relay import Node


class SQLDriverSchema(SQLAlchemyObjectType):
    class Meta:
        model = DriverSQLModel
        filter_fields = ["driverId", "carId"]
        interfaces = (Node,)


class MongoDriverSchema(MongoengineObjectType):
    class Meta:
        model = DriverMongoModel
        filter_fields = ["Activity"]
        interfaces = (Node,)
