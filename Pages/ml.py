import streamlit as st 
from Services.mlservice import monthlyfeatures, trainmodel

st.title("ML - Sales Forecasting")

# Show Features
if st.button("Show Monthly Features"):
    with st.spinner("Loading features..."):
        try:
            df = monthlyfeatures()
            st.subheader("Monthly Feature Dataset")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error: {e}")

# Train Model
if st.button("Train Model"):
    with st.spinner("Training Linear Regression model..."):
        try:
            results = trainmodel()
            st.subheader("Model Evaluation Metrics")
            st.write(f"**R² Score:** {results['r2_score']:.4f}")
            st.write(f"**MAE (Mean Absolute Error):** {results['mae']:,.2f}")
            st.write(f"**RMSE (Root Mean Squared Error):** {results['rmse']:,.2f}")
            # st.info("""
            #          **Note:** R² is negative because the model was trained on 
            #         Olist's rapid growth phase (2016-2017), but the test period (2018) 
            #         shows a plateau/decline in revenue. Linear Regression assumes one 
            #         consistent trend across all data — it cannot adapt when the underlying 
            #         pattern changes. A time-series model (Prophet/ARIMA) would handle 
            #         this better.
            #         """)
        except Exception as e:
            st.error(f"Error: {e}")