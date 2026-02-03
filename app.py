import streamlit as st
import wave
import io
import os
from piper import PiperVoice

# Page Configuration
st.set_page_config(
    page_title="Arabic TTS Demo",
    page_icon="🗣️",
    layout="centered"
)

# Title and Description
st.title("🗣️ Arabic Text-to-Speech (TTS)")
st.markdown("""
This app generates Arabic speech using **Piper TTS** models.
Choose between a **Male** and **Female** voice below.
""")

# Model Paths (Relative to app.py)
# Ensure these files are in the same directory as this script
MALE_MODEL_PATH = "ar_JO-kareem-medium.onnx"
FEMALE_MODEL_PATH = "arabic-emirati-female-model.onnx"

@st.cache_resource
def load_model(model_path, use_cuda=False):
    """
    Loads the Piper voice model. Caches the resource to avoid reloading.
    Attempts to use CUDA if requested, explicitly falling back to CPU if it fails.
    """
    if not os.path.exists(model_path):
        st.error(f"Model file not found: {model_path}")
        return None

    try:
        # Try loading with requested CUDA setting
        voice = PiperVoice.load(model_path, use_cuda=use_cuda)
        return voice
    except Exception as e:
        if use_cuda:
            st.warning(f"Failed to load model with CUDA enabled. Retrying with CPU... Error: {e}")
            try:
                # Fallback to CPU
                voice = PiperVoice.load(model_path, use_cuda=False)
                return voice
            except Exception as e2:
                st.error(f"Failed to load model on CPU as well. Error: {e2}")
                return None
        else:
            st.error(f"Failed to load model. Error: {e}")
            return None

# Sidebar / Controls
col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area(
        "Enter Arabic Text", 
        value="السلام عليكم ورحمة الله وبركاته. كيف حالك اليوم؟",
        height=150
    )

with col2:
    gender = st.radio("Select Voice", ["Male", "Female"])
    accelerate = st.checkbox("Use GPU (if available)", value=False)

if st.button("Generate Audio", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        model_path = MALE_MODEL_PATH if gender == "Male" else FEMALE_MODEL_PATH
        
        with st.spinner(f"Loading {gender} voice model..."):
            # Determine if we should try CUDA
            # Streamlit Cloud Free is CPU only, so default is fine.
            # But we respect user checkbox.
            voice = load_model(model_path, use_cuda=accelerate)
            
        if voice:
            with st.spinner("Synthesizing speech..."):
                try:
                    # Create an in-memory buffer for the audio
                    wav_buffer = io.BytesIO()
                    
                    # Piper synthesizes natively to a wave file object
                    with wave.open(wav_buffer, "wb") as wav_file:
                        # Explicitly set parameters to avoid "channels not specified" error
                        wav_file.setnchannels(1)  # Mono
                        wav_file.setsampwidth(2)  # 16-bit
                        wav_file.setframerate(voice.config.sample_rate)
                        
                        voice.synthesize_wav(text_input, wav_file)
                    
                    # Reset buffer position to beginning so we can read it
                    wav_buffer.seek(0)
                    
                    st.success("Audio generated successfully!")
                    st.audio(wav_buffer, format="audio/wav")
                    
                except Exception as e:
                    st.error(f"Error during synthesis: {e}")
