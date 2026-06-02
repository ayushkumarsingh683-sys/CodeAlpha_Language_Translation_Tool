import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# 1. Page Configuration & UI Styling
st.set_page_config(page_title="AI Language Translator", page_icon="🌐", layout="centered")

st.title("🌐 AI Language Translation Tool")
st.write("Translate text instantly between multiple languages with AI-powered audio playback.")
st.markdown("---")

# 2. Supported Languages Dictionary
languages = {
    "English": "en",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Hindi (हिन्दी)": "hi",
    "Arabic (العربية)": "ar",
    "Chinese (Mandarin)": "zh-CN",
    "Japanese (日本語)": "ja",
    "Russian (Русский)": "ru",
    "Portuguese (Português)": "pt"
}

# 3. Layout: Source and Target Language Selection
col1, col2 = st.columns(2)

with col1:
    source_lang_label = st.selectbox("From (Source Language):", list(languages.keys()), index=0)
    source_code = languages[source_lang_label]

with col2:
    target_lang_label = st.selectbox("To (Target Language):", list(languages.keys()), index=1)
    target_code = languages[target_lang_label]

# 4. Text Input Area
text_to_translate = st.text_area("Enter the text you want to translate:", height=150, placeholder="Type something here...")

# 5. Translation Logic
if st.button("Translate Text", type="primary"):
    if text_to_translate.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                # Perform translation using deep-translator API wrapper
                translated_text = GoogleTranslator(source=source_code, target=target_code).translate(text_to_translate)
                
                # Display Results
                st.markdown("### 📝 Translated Output:")
                st.success(translated_text)
                
                # Save to session state so text-to-speech works on button press without re-running translation
                st.session_state['translated_text'] = translated_text
                st.session_state['target_code'] = target_code
                
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")

# 6. Optional Features: Text-to-Speech (Audio Playback)
if 'translated_text' in st.session_state:
    st.markdown("### 🔊 Audio Features")
    if st.button("🔊 Play Translated Audio"):
        with st.spinner("Generating audio..."):
            try:
                # Convert translated text to speech
                tts = gTTS(text=st.session_state['translated_text'], lang=st.session_state['target_code'], slow=False)
                audio_file = "translated_audio.mp3"
                tts.save(audio_file)
                
                # Play audio in Streamlit app
                st.audio(audio_file, format="audio/mp3")
                
                # Clean up local audio file after playing
                os.remove(audio_file)
            except Exception as e:
                st.error("Audio feature is unavailable for this specific language combination or requires an internet connection.")