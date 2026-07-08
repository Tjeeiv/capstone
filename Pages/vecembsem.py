import streamlit as st
from Services.vectorembSem import getreviewsforembedding, generateembeddings, build_faiss_index, search_reviews

st.title("🔍 Review Knowledge Base")

if st.button("Build Knowledge Base"):
    with st.spinner("Generating embeddings and building index..."):
        try:
            df = getreviewsforembedding()
            embedded_df, vectors = generateembeddings(df)
            build_faiss_index(embedded_df, vectors)
            st.success(f"✅ Indexed {len(df)} reviews successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("Search Reviews")
query = st.text_input("Enter your search query (any language):")
if query:
    results = search_reviews(query)
    st.dataframe(results[["REVIEWID", "REVIEWCOMMENTMESSAGE"]])