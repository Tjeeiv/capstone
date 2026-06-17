import streamlit as st
from Services.datasetservice import getdata
st.title("Get dataset from source")


if st.button("Get Dataset"):
    with st.spinner("Downloading data from Kaggle.."):
        try:

            path = getdata()
        except Exception as e:
            st.error(f"Error:{e}")
