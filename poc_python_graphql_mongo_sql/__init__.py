from flask import Flask
from flask_graphql import GraphQLView
from database import sql_db_session
from graphhql.query import schema


app = Flask(__name__)
app.debug = True


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    sql_db_session.remove()


if __name__ == "__main__":
    app.run()
