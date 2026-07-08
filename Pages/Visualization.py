import streamlit as st 
from Services.visualizeservice import fetchgolddata, plottopcategories,plotmonthlytrend, plotreviewdistribution
st.title("Data visualization")

st.title("Visual Analytics")


if st.button("Generate Visualization"):
    with st.spinner("Loading Graph.."):
        try:

            sales , reviews = fetchgolddata()
 
            st.subheader("1. Top-Performing Product Categories")
            fig1 = plottopcategories(sales)
            st.pyplot(fig1)

            st.header("2. Monthly Sales Trend")
            fig2 = plotmonthlytrend(sales)
            st.pyplot(fig2)

            st.header("3. Review Distribution")
            fig3 = plotreviewdistribution(reviews)
            st.pyplot(fig3)

        except Exception as e:
            st.error(f"Error:{e}")
 