import streamlit as st
import os
from streamlit_option_menu import option_menu
from gemni_utility import load_gemini_pro_model, gemini_flash_model,embedding_model_response,gemini_pro_response
from PIL import Image

working_directory = os.path.dirname(os.path.abspath(__file__))
print(working_directory)
st.set_page_config(
    page_title="Gemini AI",
    page_icon='🧠',
    layout="centered"
)

with st.sidebar:
    selected = option_menu(
        menu_title="Gemini AI",
        options=["ChatBot", "Image Captioning", "Embed text", "Ask me anything"],
        menu_icon='robot',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0
    )

# Function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# Chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()
    # Initialize chat session in streamlit if not already present
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    # Streamlit page title
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image captioning page
if selected == 'Image Captioning':
    # Streamlit page title
    st.title("📷 Snap Narrate")
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    # Ensure an image is uploaded before processing
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "Write a short caption for this image."

        # Get the response from gemini-flash model
        caption = gemini_flash_model(default_prompt, image)

        with col2:
            st.info(caption)
    else:
        st.warning("Please upload an image to generate a caption.")


#text embedding page

if selected=="Embed text":
    st.title("🔡 Embed Text")

    #input text box
    input_text=st.text_area(label="",placeholder="Enter the text to get the embeddings")
    if st.button("Get Embeddings"):
        response=embedding_model_response(input_text)
        st.markdown(response)


#question answering page
if selected =="Ask me anything":
    st.title(" ❓Ask me a question ")
    #text box to enter prompt
    user_prompt=st.text_area(label="",placeholder="Ask Gemini-Pro...")
    if st.button("Get an answer"):
        response=gemini_pro_response(user_prompt)
        st.markdown(response)

