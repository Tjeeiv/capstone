import streamlit as st 
from Services.mlservice import monthlyfeatures,trainmodel


st.title("ML")

if st.button("Feature Dataset"):
    with st.spinner("loading data"):
        try:
            df = monthlyfeatures()
            st.dataframe(df)
            modelscore = trainmodel()
            st.write(modelscore)
        except Exception as e:
            st.error(f"Error:{e}")