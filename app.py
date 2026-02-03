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
This app generates Arabic speech using **TTS** models.
Choose between a **Male** and **Female** voice below.
""")

# Model Paths (Relative to app.py)
# Ensure these files are in the same directory as this script
MALE_MODEL_PATH = "ar_JO-kareem-medium.onnx"
FEMALE_MODEL_PATH = "arabic-emirati-female-model.onnx"

@st.cache_resource
def load_model(model_path):
    """
    Loads the Piper voice model. Caches the resource to avoid reloading.
    Automatically attempts to use CUDA first, falling back to CPU.
    """
    if not os.path.exists(model_path):
        st.error(f"Model file not found: {model_path}")
        return None

    # Try CUDA first if available (common check)
    try:
        if "CUDAExecutionProvider" in import_onnx_providers():
             voice = PiperVoice.load(model_path, use_cuda=True)
             print(f"Loaded {model_path} with CUDA")
             return voice
    except Exception:
        pass # Fallthrough to CPU
        
    try:
        # Default/Fallback to CPU
        voice = PiperVoice.load(model_path, use_cuda=False)
        print(f"Loaded {model_path} with CPU")
        return voice
    except Exception as e:
        st.error(f"Failed to load model. Error: {e}")
        return None

def import_onnx_providers():
    try:
        import onnxruntime
        return onnxruntime.get_available_providers()
    except:
        return []

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
    # Speed Control: 1.0 is normal. Higher is faster? Piper uses 'length_scale'.
    # length_scale > 1 is slow, < 1 is fast. 
    # Let's present "Speed" to user: 0.5x (slow) to 2.0x (fast).
    # length_scale = 1 / speed
    speed = st.slider("Speech Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1, help="Higher is faster")

if st.button("Generate Audio", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        model_path = MALE_MODEL_PATH if gender == "Male" else FEMALE_MODEL_PATH
        
        with st.spinner(f"Loading {gender} voice model..."):
            voice = load_model(model_path)
            
        if voice:
            with st.spinner("Synthesizing speech..."):
                try:
                    # Calculate length_scale from speed
                    length_scale = 1.0 / speed
                    
                    # Create synthesis config
                    from piper import SynthesisConfig
                    syn_config = SynthesisConfig(length_scale=length_scale)

                    # Create an in-memory buffer for the audio
                    wav_buffer = io.BytesIO()
                    
                    # Piper synthesizes natively to a wave file object
                    with wave.open(wav_buffer, "wb") as wav_file:
                        # Explicitly set parameters to avoid "channels not specified" error
                        wav_file.setnchannels(1)  # Mono
                        wav_file.setsampwidth(2)  # 16-bit
                        wav_file.setframerate(voice.config.sample_rate)
                        
                        voice.synthesize_wav(text_input, wav_file, syn_config=syn_config)
                    
                    # Reset buffer position to beginning so we can read it
                    wav_buffer.seek(0)
                    
                    st.success("Audio generated successfully!")
                    st.audio(wav_buffer, format="audio/wav")
                    
                except Exception as e:
                    st.error(f"Error during synthesis: {e}")
