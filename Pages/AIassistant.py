import streamlit as st
import requests

st.title("🤖 AI Review Assistant")
st.write("Ask questions about customer reviews — powered by RAG + AI")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
question = st.chat_input("Ask about customer reviews...")

if question:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Call /ask-assistant API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask-assistant",
                    json={"question": question},
                    timeout=120
                )
                result = response.json()
                answer = result["answer"]
                sources = result["sources"]

                st.write(answer)

                with st.expander("📄 Source Reviews Used"):
                    for i, source in enumerate(sources, 1):
                        st.write(f"{i}. {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error calling API: {e}")