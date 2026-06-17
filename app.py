import streamlit as st

st.set_page_config(page_title="CapStone", layout= "wide")

st.title("DE & GenAI")

st.write("Welcome! Use the sidebar to navigate through each step.")

st.markdown("""
### Steps:
1. 📥 **Get Dataset** — Download data from Kaggle
2. 💾 **Store Excel** — Save data into DB as Excel
3. 🧹 **Clean Data** — Clean and store in table
4. 📈 **Visualize** — View charts and insights
""")