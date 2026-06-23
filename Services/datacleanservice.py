import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from Services.snowflakeconnector import get_snowflake_connection

def readtable(conn, schema, table):
    df = pd.read_sql(f"SELECT * FROM {schema}.{table}", conn)
    
    # Auto-detect and convert likely datetime columns
    for col in df.columns:
        if "DATE" in col or "TIMESTAMP" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    
    return df

def writetable(conn, df, schema, table):
    cs= conn.cursor()
    cs.execute(f"use schema {schema}")
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name= table, schema= schema , auto_create_table=True, overwrite= True)
    cs.close()

    return success, nrows

def cleanorders(conn):
    df= readtable(conn, "BRONZE", "ORDERS")

    datecols = [  "ORDERPURCHASETIMESTAMP", "ORDERAPPROVEDAT",
        "ORDERDELIVEREDCARRIERDATE", "ORDERDELIVEREDCUSTOMERDATE",
        "ORDERESTIMATEDDELIVERYDATE"]
    for col in datecols:
        df[col] = pd.to_datetime(df[col] , errors= "coerce")
    
    df = df .dropna(subset=["ORDERID"]).drop_duplicates()

    writetable(conn,df , "SILVER" , "ORDERS")
    return len(df)
 


def cleanorderitems(conn):
    df = readtable(conn, "BRONZE", "ORDERITEMS")

    df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")
    df["FREIGHTVALUE"] = pd.to_numeric(df["FREIGHTVALUE"], errors="coerce")
    df["SHIPPINGLIMITDATE"] = pd.to_datetime(df["SHIPPINGLIMITDATE"], errors="coerce")

    df = df.dropna(subset=["ORDERID", "PRODUCTID"]).drop_duplicates()
    writetable(conn, df, "SILVER", "ORDERITEMS")
    return len(df)


def cleanproducts(conn):
    products = readtable(conn, "BRONZE", "PRODUCTS")
    translation = readtable(conn, "BRONZE", "PRODUCTCATEGORYENGLISH")

    products = products.merge(translation, on="PRODUCTCATEGORYNAME", how="left")
    products["PRODUCTCATEGORY"] = products["PRODUCTCATEGORYNAMEENGLISH"].fillna(products["PRODUCTCATEGORYNAME"])

    products = products[[
        "PRODUCTID", "PRODUCTCATEGORY", "PRODUCTWEIGHTG",
        "PRODUCTLENGTHCM", "PRODUCTHEIGHTCM", "PRODUCTWIDTHCM"
    ]]
    products = products.dropna(subset=["PRODUCTID"]).drop_duplicates()

    writetable(conn, products, "SILVER", "PRODUCTS")
    return len(products)

def cleanorderreviews(conn):
    df = readtable(conn, "BRONZE", "ORDERREVIEW")

    df["REVIEWCREATIONDATE"] = pd.to_datetime(df["REVIEWCREATIONDATE"], errors="coerce")
    df["REVIEWANSWERTIMESTAMP"] = pd.to_datetime(df["REVIEWANSWERTIMESTAMP"], errors="coerce")
    df["REVIEWSCORE"] = pd.to_numeric(df["REVIEWSCORE"], errors="coerce")

    df = df.dropna(subset=["REVIEWID", "ORDERID", "REVIEWSCORE"]).drop_duplicates()
 
    writetable(conn, df, "SILVER", "ORDERREVIEW")
    return len(df)
def cleandata():
    conn = get_snowflake_connection()
    try:
        results = {
            # "Orders": cleanorders(conn),
            # "OrderItems": cleanorderitems(conn),
            # "Products": cleanproducts(conn),
            "OrderReview": cleanorderreviews(conn)
        }
    finally:
        conn.close()
    return results

def buildgoldsales(conn):
    orders = readtable(conn, "SILVER", "ORDERS")
    items = readtable(conn, "SILVER", "ORDERITEMS")
    products = readtable(conn, "SILVER", "PRODUCTS")

    df = orders.merge(items, on="ORDERID").merge(products, on="PRODUCTID")
    df = df[df["ORDERSTATUS"] == "delivered"]

    # Force conversion to datetime before using .dt
    df["ORDERPURCHASETIMESTAMP"] = pd.to_datetime(df["ORDERPURCHASETIMESTAMP"], errors="coerce")

    df["ORDERMONTH"] = df["ORDERPURCHASETIMESTAMP"].dt.to_period("M").astype(str)
    df["TOTALREVENUE"] = df["PRICE"] + df["FREIGHTVALUE"]

    gold = df[[
        "ORDERID", "ORDERPURCHASETIMESTAMP", "ORDERMONTH",
        "PRODUCTID", "PRODUCTCATEGORY", "PRICE", "FREIGHTVALUE", "TOTALREVENUE"
    ]]

    writetable(conn, gold, "GOLD", "SALESDATA")
    return len(gold)


def buildgoldreviews(conn):
    reviews = readtable(conn, "SILVER", "ORDERREVIEW")
    items = readtable(conn, "SILVER", "ORDERITEMS")
    products = readtable(conn, "SILVER", "PRODUCTS")

    df = reviews.merge(items, on="ORDERID").merge(products, on="PRODUCTID")

    gold = df[[
        "REVIEWID", "ORDERID", "PRODUCTID", "PRODUCTCATEGORY",
        "REVIEWSCORE", "REVIEWCOMMENTMESSAGE", "REVIEWCREATIONDATE"
    ]]

    writetable(conn, gold, "GOLD", "REVIEWSDATA")
    return len(gold)


def buildgold():
    conn = get_snowflake_connection()
    try:
        results = {
            "SalesData": buildgoldsales(conn),
            "ReviewsData": buildgoldreviews(conn),
        }
    finally:
        conn.close()
    return results
