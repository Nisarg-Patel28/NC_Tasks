import streamlit as st
from summarizer import extractive_summarize

st.set_page_config(page_title="Extractive Summarizer", layout="centered")

st.title("Task-3 Extractive Summarizer Bot")
st.write("A short introduction of this .. This tool generate a concise summary be selecting key sentences from the original text.")

text_input = st.text_area("Please enter here", height=250, placeholder="You can paste or write a paragraph or an article")

num_sentences = st.slider("Select the number of sentences in the summary", 1,10,20)

if st.button("Generate the summary"):
    if text_input.strip():
        summary = extractive_summarize(text_input, num_sentences)
        st.subheader("SUMMARY IS:")
        st.write(summary)
    else:
        st.warning("WARNING !! You may need to enter some text to summarize")