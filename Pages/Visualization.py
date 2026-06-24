import streamlit as st 
from Services.visualizeservice import fetchgolddata, plottopcategories

st.title("Data visualization")

st.title("Visual Analytics")


if st.button("Generate Visualization"):
    with st.spinner("Loading Graph.."):
        try:

            sales , reviews = fetchgolddata()
 
            st.subheader("1. Top-Performing Product Categories")
            fig1 = plottopcategories(sales)
            st.pyplot(fig1)


        except Exception as e:
            st.error(f"Error:{e}")
 