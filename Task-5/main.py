import streamlit as st
import google.generativeai as genai
from PIL import Image #Pillow library basically used for generating Images
import os
from dotenv import load_dotenv

# Loading the API KEY
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="AIzaSyDawno8MX-BuRVjzORq864Z6ZIdOBn057M")

# Loading the model
text_model = genai.GenerativeModel("gemini-2.5-flash")
vision_model = genai.GenerativeModel("gemini-2.5-pro")

# Text - Only
def generate_text_response(user_input):
    try:
        response = text_model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Text and Image both
def process_image_input(image_file, question="Describe the image"):
    try:
        image = Image.open(image_file)  
        image_file.seek(0) #seek is used to rewind file pointer after PIL reading is done.
        image_bytes = image_file.read()

        input_parts = [
            {"mime_type": image_file.type, "data": image_bytes},
            {"text": question}
        ]

        response = vision_model.generate_content(input_parts)
        return response.text
    except Exception as e:
        return f"Error in giving image: {e}"

st.set_page_config(page_title="Multi Modal Chatbot", layout = "wide")
st.title("Created a multi-modal chatbot using Google Gemini-AI")

tab1,tab2 = st.tabs(["Text chat","Image Chat"])

#1. tab1 for text input
with tab1:
    user_input = st.text_input("Enter your message:")
    if st.button("Send"):
        if user_input.strip():
            st.subheader("Response:")
            response = generate_text_response(user_input)
            st.write(response)
        else:
            st.warning("Null Text Not allowed .. Please enter a message")

#2. tab2 for image input
with tab2:
    uploaded_file = st.file_uploader("Upload image", type =["jpg","jpeg","png"])
    que = st.text_input("Ask the question about the image:", placeholder ="Describe the image.")

    if st.button("Check/Analyze the image"):
        if uploaded_file:
            st.image(uploaded_file, caption = "Uploaded Image", use_container_width="True")
            st.subheader("Response:")
            reslt = process_image_input(uploaded_file, que)
            st.write(reslt)
        else:
            st.warning("You must upload the image!")