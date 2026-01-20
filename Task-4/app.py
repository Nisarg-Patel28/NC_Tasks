import streamlit as st
from chatbot import retrieve_context

st.set_page_config(page_title="Dynamic knowledge Chatbot")
st.title("Dynamic knowledge chatbot")

user_input = st.text_input("Ask a question:")

if st.button("Ask") and user_input:
    context = retrieve_context(user_input)
    st.subheader("Answer is:")
    st.write (" ".join(context))

st.info("Add new text files to the 'data' folder and re-run updater.py to expand knowledge.")