import streamlit as st
from Services.datasetservice import getdata
from Services.datacleanservice import cleandata , buildgold
st.title("Get dataset from source")


if st.button("Get Dataset"):
    with st.spinner("Downloading data from Kaggle.."):
        try:

            uploadedfiles = getdata()

            st.write(f"Number of files uploaded : {len(uploadedfiles) }")
            st.write("***Files***", uploadedfiles)



        except Exception as e:
            st.error(f"Error:{e}")

if st.button("Clean Data"):
    with st.spinner("Cleaning Inprogress.."):
        try:

            results = cleandata()
            st.write(f"Number of files uploaded : {results }")
            goldresult = buildgold()
           
            st.write(f"Number of files uploaded : {goldresult }")
             

            

        except Exception as e:
            st.error(f"Error:{e}")