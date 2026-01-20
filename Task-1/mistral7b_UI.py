import streamlit as st
from mistral7b_AGC import get_article

st.set_page_config(page_title = "Article generator chatbot", page_icon="🤖", layout="centered")

st.title("📄 Article generator chatbot using Mistral 7b Model")
st.write("Generate articles")

topic = st.text_area("Enter topic:", height=200, placeholder ="eg. Impact of AI on EV cars.")
length = st.slider("Select the article length (words)",min_value= 100,max_value= 2000, value=500, step = 100)

if st.button("Generate the article"):
    if topic.strip():
        with st.spinner("Wait for a moment. The article is being generating"):
            prompt = f"Write article about {topic}. The article should be roughly {length} words."
            article = get_article(prompt)
        st.subheader("The generated article is:")
        st.write(article)
    else:
        st.warning("You must enter the topic of the article")
