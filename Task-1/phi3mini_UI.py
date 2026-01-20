import streamlit as st
from phi3mini_AGC import get_article

st.set_page_config(page_title="Article Generator Chatbot", page_icon = "📄", layout="centered")

st.title("Article Generator Chatbot Using Phi3:mini model")

topic = st.text_input("Enter the topic of the article:")
count_word = st.slider("Select word count", min_value=100, max_value = 1000, value=300, step=20)

if st.button("Generate the article"):
    if topic.strip() == "":
        st.warning("You must enter the topic of the article!")
    else:
        with st.spinner("Wait for a moment..The article is generating"):
            prompt = f"Write an article about {topic} and limit it to {count_word} words."
            article = get_article(prompt)
            st.subheader("Generated Article is")
            st.write(article)