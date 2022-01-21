# Python graphql with mongo and sql POC

This code is an example on how to create GraphQL queries that feed from different data sources, in this specific example, from Mongo and SQL.

## Installation
I recomed using a virutal env, which you can set up using:
```bash
python3 -m venv env
source env/bin/activate
```

You can also add system variables to the venv/bin/activate to make sure they are available for your tests.

You can use pip3 to install the needed packages:
```bash
pip3 -m install <pacakage_name> 
```

Flask==2.0.2
Flask-GraphQL==2.0.1
Flask-Script==2.0.6
Flask-SQLAlchemy==2.5.1
graphene==2.1.8
graphene-mongo==0.2.13
graphene-sqlalchemy==2.2.2
graphql-core==2.3.1
graphql-relay==2.0.1
graphql-server-core==1.2.0
mongoengine==0.23.1
pymongo==3.12.3
pyodbc==4.0.32
pytest==6.2.5
requests==2.27.1
SQLAlchemy==1.4.0


Also, you need to configure the FreeTDS driver in order for this code to work. Here is a useful link on how to do that: https://gist.github.com/Bouke/10454272

##GraphQL examples
```graphql
{
  getDrivers {
    driverId
    field1
    field2
    field3
  }
}


{
  getDriversById(driverId: "1234") {
    driverId
    field1
    field2
    field3
  }
}


{
  getDriverAndTractorsById(driverId:"1234", carId:"57631") {
    driverId
    carId
    driver {
    	driverId
		field1
		field2
		field3
    }
    cars{
		  driverId
		  field1
		  field2
		  field3
    }

  }
}
```
