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
    ax.ticklabel_format(style='plain', axis='x')
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Category")
    ax.set_title(f"Top {top_n} Performing Product Categories by Revenue")
    plt.tight_layout()
    return fig



def plotmonthlytrend(sales_df):
    data = sales_df.groupby("ORDERMONTH")["TOTALREVENUE"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data.index ,data.values, marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Monthly Revenue Trend"    )
    plt.xticks(rotation = 45)
    plt.tight_layout()
    return fig

def plotreviewdistribution(reviewdf):

    fig,ax = plt.subplots(figsize = (10,5))
    sns.countplot(data=reviewdf , x="REVIEWSCORE",ax=ax)
    ax.set_xlabel("Review")
    ax.set_ylabel("Total count")
    ax.set_title("Review Distribution"    )     
    return fig