import pandas as pd
from Services.visualizeservice import fetchgolddata
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
MODEL_DIR = "./models"
os.makedirs(MODEL_DIR, exist_ok=True)
"""
Feature preparation: one row per month
Aggregate per month: total revenue, count of orders, average revenue, month number
"""

def monthlyfeatures():
    sales, reviews = fetchgolddata()

    monthdf = sales.groupby("ORDERMONTH").agg(
        monthrev=("TOTALREVENUE", "sum"),
        monthorderitemcount=("TOTALREVENUE", "count"),
        monthordercount=("ORDERID", "nunique"),
        monthavgrevenue=("TOTALREVENUE", "mean")
    )

    # Fix missing months (e.g. 2016-11 had no data, causes wrong shift() pairing)
    monthdf.index = pd.to_datetime(monthdf.index, format="%Y-%m")
    full_range = pd.date_range(start=monthdf.index.min(), end=monthdf.index.max(), freq="MS")
    monthdf = monthdf.reindex(full_range, fill_value=0)
    monthdf.index = monthdf.index.strftime("%Y-%m")
    monthdf.index.name = "ORDERMONTH"

    monthdf["monthnumber"] = pd.to_datetime(monthdf.index, format="%Y-%m").month

    return monthdf


# def trainmodel():
#     df = monthlyfeatures()

#     encode = pd.get_dummies(df["monthnumber"], prefix="month")
#     df = pd.concat([df, encode], axis=1)
#     df = df.drop(columns=["monthnumber"])

#     df["targetnextmonthrevenue"] = df["monthrev"].shift(-1)
#     df = df.dropna(subset=["targetnextmonthrevenue"])

#     X = df.drop(columns=["targetnextmonthrevenue"])
#     y = df["targetnextmonthrevenue"]

#     scaler = StandardScaler()
#     numeric_cols = ["monthrev", "monthorderitemcount", "monthordercount", "monthavgrevenue"]
#     X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

#     model = LinearRegression()
#     model.fit(X_train, y_train)

#     predictions = model.predict(X_test)

#     return {
#         "r2_score": r2_score(y_test, predictions),
#         "mae": mean_absolute_error(y_test, predictions),
#         "rmse": mean_squared_error(y_test, predictions) ** 0.5
#     }


def trainandsave():
    df = monthlyfeatures()

    encode = pd.get_dummies(df["monthnumber"], prefix="month")
    df = pd.concat([df, encode], axis=1)
    df = df.drop(columns=["monthnumber"])

    df["targetnextmonthrevenue"] = df["monthrev"].shift(-1)
    df = df.dropna(subset=["targetnextmonthrevenue"])

    X = df.drop(columns=["targetnextmonthrevenue"])
    y = df["targetnextmonthrevenue"]

    scaler = StandardScaler()
    numeric_cols = ["monthrev", "monthorderitemcount", "monthordercount", "monthavgrevenue"]
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, f"{MODEL_DIR}/linear_regression.pkl")
    joblib.dump(scaler, f"{MODEL_DIR}/scaler.pkl")
    joblib.dump(list(X.columns), f"{MODEL_DIR}/feature_columns.pkl")

    predictions = model.predict(X_test)

    return {
        "r2_score": r2_score(y_test, predictions),
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions) ** 0.5
    }

def predictrevenue(input_features: dict):
    model = joblib.load(f"{MODEL_DIR}/linear_regression.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    feature_columns = joblib.load(f"{MODEL_DIR}/feature_columns.pkl")

    df = pd.DataFrame([input_features])
    df = df.reindex(columns=feature_columns, fill_value=0)

    numeric_cols = ["monthrev", "monthorderitemcount", "monthordercount", "monthavgrevenue"]
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    prediction = model.predict(df)
    return float(prediction[0])