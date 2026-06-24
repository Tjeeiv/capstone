import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Services.snowflakeconnector import get_snowflake_connection
from Services.datacleanservice import readtable



def fetchgolddata():
    conn = get_snowflake_connection()
    try:
        sales = readtable(conn, "GOLD", "SALESDATA")
        reviews= readtable(conn, "GOLD","REVIEWSDATA")
    finally:
        conn.close()
    return sales, reviews


def plottopcategories(sales_df, top_n=10):
    top = (
        sales_df.groupby("PRODUCTCATEGORY")["TOTALREVENUE"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, ax=ax, palette="viridis")
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Category")
    ax.set_title(f"Top {top_n} Performing Product Categories by Revenue")
    plt.tight_layout()
    return fig