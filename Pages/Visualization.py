import streamlit as st 
st.title("Data visualization")


if st.button("Graph"):
    with st.spinner("Loading Graph.."):
        try:

            

            st.write(f"Number of files uploaded :  ")
            st.write("***Files***",  )



        except Exception as e:
            st.error(f"Error:{e}")
 