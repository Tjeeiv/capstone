import streamlit as st
import requests
from Services.visualizeservice import fetchgolddata, plottopcategories, plotmonthlytrend, plotreviewdistribution

st.title("📊 Business Dashboard")

# Section 1: Charts
st.header("Sales Analytics")

if st.button("Load Charts"):
    with st.spinner("Loading visualizations..."):
        try:
            sales, reviews = fetchgolddata()

            st.subheader("1. Top Performing Product Categories")
            fig1 = plottopcategories(sales)
            st.pyplot(fig1)

            st.subheader("2. Monthly Sales Trend")
            fig2 = plotmonthlytrend(sales)
            st.pyplot(fig2)

            st.subheader("3. Distribution of Review Ratings")
            fig3 = plotreviewdistribution(reviews)
            st.pyplot(fig3)

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# Section 2: Sales Prediction Form
st.header("Revenue Forecast")
st.write("Enter last month's figures to predict next month's revenue:")

col1, col2 = st.columns(2)

with col1:
    monthrev = st.number_input("Last Month Revenue", min_value=0.0, value=1200000.0)
    monthordercount = st.number_input("Order Count", min_value=0, value=850)

with col2:
    monthorderitemcount = st.number_input("Order Item Count", min_value=0, value=1500)
    monthavgrevenue = st.number_input("Avg Order Revenue", min_value=0.0, value=800.0)

monthnumber = st.slider("Month Number (1=Jan, 12=Dec)", min_value=1, max_value=12, value=9)

if st.button("Predict Next Month Revenue"):
    with st.spinner("Calling prediction API..."):
        try:
            payload = {
                "monthrev": monthrev,
                "monthorderitemcount": monthorderitemcount,
                "monthordercount": monthordercount,
                "monthavgrevenue": monthavgrevenue,
                "monthnumber": monthnumber
            }
            response = requests.post("http://localhost:8000/predict-sales", json=payload)
            result = response.json()
            st.success(f"💰 Predicted Revenue: R$ {result['predicted_revenue']:,.2f}")
        except Exception as e:
            st.error(f"Error: {e}")