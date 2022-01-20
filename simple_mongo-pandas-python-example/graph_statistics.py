import pandas as pd
import mongo_utils as mngu
import matplotlib.pyplot as plt
import sql_utils as sqlu

_MNG_DATABASE = "dbstats"
_MNG_TABLES_COLLECTION = "tablestats"
_MNG_TABLES_XAXIS = "TableName"
_MNG_TABLES_YAXIS = "SizeInMB"
_MNG_SCHEMA_COLLECTION = "schemastats"


mngu.get_and_store_info("dbstats", sqlu.query_tables(), "tablestats")

mngu.get_and_store_info("dbstats", sqlu.query_schema(), "schemastats")


def graph(data, xaxis, yaxis, xlabel, ylabel):
    plt.close("all")

    try:
        print("***** data to graph ****")
        print(data)
        data.plot(x=xaxis, y=yaxis, kind="barh", fontsize=7, ylabel=ylabel)
        plt.show()

    except Exception as e:
        print(str(e))


def graph_median(values, xaxis, yaxis, xlabel, ylabel):
    try:
        graph(
            data=values.groupby(xaxis)[yaxis].median().sort_values(0),
            xaxis=xaxis,
            yaxis=yaxis,
            xlabel=xlabel,
            ylabel=ylabel,
        )

    except Exception as e:
        print(str(e))


def graph_average(values, xaxis, yaxis, xlabel, ylabel):
    try:
        graph(
            data=values.groupby(xaxis)[yaxis].mean().sort_values(0),
            xaxis=xaxis,
            yaxis=yaxis,
            xlabel=xlabel,
            ylabel=ylabel,
        )

    except Exception as e:
        print(str(e))


def graph_max(values, xaxis, yaxis, xlabel, ylabel):
    try:
        graph(
            data=values.groupby(xaxis)[yaxis].max().sort_values(0),
            xaxis=xaxis,
            yaxis=yaxis,
            xlabel=xlabel,
            ylabel=ylabel,
        )

    except Exception as e:
        print(str(e))


def graph_min(values, xaxis, yaxis, xlabel, ylabel):
    try:
        graph(
            data=values.groupby(xaxis)[yaxis].min().sort_values(0),
            xaxis=xaxis,
            yaxis=yaxis,
            xlabel=xlabel,
            ylabel=ylabel,
        )

    except Exception as e:
        print(str(e))


graph_average(
    values=pd.DataFrame(mngu.read_statistics(_MNG_DATABASE, _MNG_TABLES_COLLECTION)),
    xaxis=_MNG_TABLES_XAXIS,
    yaxis=_MNG_TABLES_YAXIS,
    xlabel=_MNG_TABLES_XAXIS,
    ylabel=_MNG_TABLES_YAXIS,
)
