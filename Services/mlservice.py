import pandas as pd;
from Services.visualizeservice import fetchgolddata
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

"""
feature preparation one row per month 
from sales data aggregate per month total revenue, count of orders, average revenue, month number
"""
def monthlyfeatures():

     sales, reviews = fetchgolddata()

     monthdf = sales.groupby("ORDERMONTH").agg(
          monthrev = ("TOTALREVENUE","sum"),
          monthorderitemcount = ("TOTALREVENUE" , "count"),
          monthordercount = ("ORDERID" , "nunique"),
          monthavgrevenue= ("TOTALREVENUE","mean")
     )
     monthdf["monthnumber"] = pd.to_datetime(monthdf.index, format="%Y-%m").month
     
     return monthdf

def trainmodel():
     df = monthlyfeatures()

     encode = pd.get_dummies(df["monthnumber"], prefix="month")

     df = pd.concat([df,encode] , axis = 1)
     df= df.drop(columns =["monthnumber"])
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

     predictions = model.predict(X_test)

     accuracy = r2_score(y_test, predictions)
     mae = mean_absolute_error(y_test, predictions)
     rmse = mean_squared_error(y_test, predictions) ** 0.5

     return {
    "r2_score": accuracy,
    "mae": mae,
    "rmse": rmse
}