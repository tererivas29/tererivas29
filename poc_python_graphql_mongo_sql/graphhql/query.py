import graphene
from graphql import GraphQLError
from graphhql.models import DriverSQLModel, DriverMongoModel
from graphhql.schemas import SQLDriverSchema, MongoDriverSchema


class DriversCarsSchema(graphene.ObjectType):
    driverId = graphene.String()
    carId = graphene.String()
    driver = graphene.List(SQLDriverSchema)
    cars = graphene.List(MongoDriverSchema)

    def resolve_driver(self, info):
        if self.driverId:
            driver_query = SQLDriverSchema.get_query(info)
            self.driver = driver_query.filter(
                DriverSQLModel.driverId.contains(self.driverId),
                DriverSQLModel.field1.contains(self.field1),
            ).all()
            return self.driver
        else:
            raise GraphQLError("driverId argument is required.")

    def resolve_cars(self, info):
        if self.carId:
            self.cars = DriverMongoModel.objects.filter(
                carId=self.carId
            )[:20]
            return self.cars
        else:
            raise GraphQLError("carId argument is required.")


class Query(graphene.ObjectType):
    get_drivers = graphene.List(SQLDriverSchema)
    get_drivers_by_id = graphene.List(SQLDriverSchema, driverId=graphene.String())
    get_drivers_by_activity = graphene.List(
        MongoDriverSchema, activity=graphene.String()
    )
    get_driver_and_cars_by_id = graphene.Field(
        DriversCarsSchema,
        driverId=graphene.String(),
        carId=graphene.String(),
    )

    @staticmethod
    def resolve_get_drivers(parent, info, **kwargs):
        return (
            SQLDriverSchema.get_query(info).order_by("driverId").limit(20).offset(1).all()
        )

    @staticmethod
    def resolve_get_drivers_by_id(parent, info, **kwargs):
        driverId = kwargs.get("driverId")
        if driverId:
            driver_query = SQLDriverSchema.get_query(info)
            return driver_query.filter(DriverSQLModel.driverId.contains(driverId)).all()
        else:
            raise GraphQLError("driverId argument is required.")

    @staticmethod
    def resolve_get_drivers_by_activity(parent, info, **kwargs):
        activity = kwargs.get("activity")
        if activity:
            return DriverMongoModel.objects.filter(Activity=activity)[:20]
        else:
            raise GraphQLError("activity argument is required.")

    @staticmethod
    def resolve_get_driver_and_cars_by_id(parent, info, **kwargs):
        return DriversCarsSchema(kwargs.get("driverId"), kwargs.get("tractorNumber"))


schema = graphene.Schema(query=Query)
