import streamlit as st
from PIL import Image
import google.generativeai as genai
from gtts import gTTS
from deep_translator import GoogleTranslator

# Streamlit app
st.title("AI Image Description & Translation")
st.write("Upload an image and enter a prompt. The model will generate a description based on your prompt.")

# Upload image and enter prompt
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
user_prompt = st.text_input("Enter your prompt:", value="")

# Initialize session state variables if not already initialized
if 'description' not in st.session_state:
    st.session_state.description = ""

# Function to generate audio using gTTS
def generate_audio(text, lang='en', gender='female', filename="output.mp3"):
    if text:  # Ensure there is text to convert to speech
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
    else:
        st.error("No description text available to convert to audio.")

# Function to translate description to another language
def change_language(language):
    translated_text = GoogleTranslator(source='auto', target=language).translate(st.session_state.description)
    return translated_text

# Check if both an image and prompt are provided
if uploaded_file and user_prompt:
    try:
        if st.session_state.description == "":
            # Configure API with your key
            api_key = ""  # Replace with your actual API key
            genai.configure(api_key=api_key)

            # Initialize the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.session_state.img = Image.open(uploaded_file)

            # Generate description based on user prompt and image
            response = model.generate_content([user_prompt, st.session_state.img])
            st.session_state.description = response.text

        # Display image and generated description
        st.image(st.session_state.img, caption='Uploaded Image', use_column_width=True)
        st.write(st.session_state.description)

    except Exception as e:
        st.error(f"Error processing the image: {e}")

else:
    if not uploaded_file:
        st.write("No image file selected.")
    if not user_prompt:
        st.write("Please enter a prompt.")

# Voice selection and audio generation for original description
# Now only showing Female as the available option for voice
voice_choice = st.selectbox("Choose a voice for description:", ["Female"])  # Only Female option
if voice_choice and st.session_state.description:
    generate_audio(st.session_state.description, gender='female')  # Always using female voice
    st.audio("output.mp3", format='audio/mp3')

# Language translation selection
lang_choice = st.selectbox("Choose a Language to Translate:", ["None", "English", "Hindi", "Odia", "Telugu", "Tamil", "Punjabi", "Malayalam", "Marathi", "Kannada"])
if lang_choice != "None":
    lang_code = {'English': 'en', 'Hindi': 'hi', 'Odia': 'or', 'Telugu': 'te', 'Tamil': 'ta', 'Punjabi': 'pa', 'Malayalam': 'ml', 'Marathi': 'mr', 'Kannada': 'kn'}[lang_choice]
    translated_text = change_language(lang_code)
    st.write(translated_text)

    # Generate and play audio for the translated text
    translated_filename = "translated_output.mp3"
    generate_audio(translated_text, lang=lang_code, gender='female', filename=translated_filename)  # Always female voice for translation
    
    # Play button for translated audio
    if st.button('Play Translated Audio'):
        st.audio(translated_filename, format='audio/mp3')
