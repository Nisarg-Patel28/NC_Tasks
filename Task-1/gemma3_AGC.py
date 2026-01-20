import streamlit as st #Streamlit used for UI of the bot
from ollama import Client #Ollama 

client = Client() #This line is used for making connection with the Ollama server, sends the request to the model and receieves responses

#Generating the article of the chatbot
def get_article(topic, length):
    prompt = f"Write the topic {length} on which {topic} you want the article."
    response = client.chat(model="gemma3:4b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

st.title("Article generator chatbot using Ollama-Gemma3")
st.write("Generating article")

topic = st.text_input("Enter the article topic:", placeholder = "eg. Impact of Artificial Intelligence in Healthcare Industry")
length = st.slider("Article length(words)", min_value=150, max_value=1000, value=500, step=40)

if st.button("Generate the article"):
    if topic.strip():
        with st.spinner("Wait for few minutes!"):
            article = get_article(topic,length)
        st.subheader("The Generated Article is:")
        st.write(article)
    else:
        st.warning("Enter the topic for which you want the article.")