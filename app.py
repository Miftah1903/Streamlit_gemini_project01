import streamlit as st 
from google import genai
import os
from dotenv import load_dotenv 
from PIL import Image
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#title
st.title("AI Code Debugger App")
st.markdown("Upload your code error screenshot to find bugs and get solutions.")
st.divider()

#sidebar
with st.sidebar:
    st.header("Controls")
    #image uploader
    images=st.file_uploader(
        "Upload the ss of your error",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    if images:
        st.subheader("Uploaded Image")
        st.image(images)
    #option bar
    selected_option=st.selectbox(
        "Select what do you want",
        ("Hints", "Solution with code"),
        index=None,
        placeholder="Choose an option..."
    )
    
    #button
    pressed=st.button("Debug Code", type="primary")
if pressed:
        if not images:    
            st.error("Please upload an image before debugging.")
        if not selected_option:
            st.error("Please select an option before debugging.")
        #container
        if images and selected_option:
            with st.container(border=True):
                st.subheader(f"AI {selected_option}")
            #loading
            with st.spinner("Gemini is analyzing the code..."):
                try:
                    pil_images = [Image.open(image) for image in images]
                    
                    # Prompt selection based on user choice
                    if selected_option == "Hints":
                        prompt = "Look at this code screenshot and provide short hints to fix the error. Do not give the full code."
                    else:
                        prompt = "Look at this code screenshot, explain the bug, and provide the full corrected code."
                    #api call
                    response=client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=[prompt,*pil_images] # Assuming the first image is used for analysis            
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                
            
    
    