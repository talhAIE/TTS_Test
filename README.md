# Arabic TTS Streamlit App

This is a simple Streamlit app to generate Arabic speech using Piper TTS.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Deployment to Streamlit Cloud

1.  Push this entire directory (including the `.onnx` and `.json` model files) to a GitHub repository.
2.  Go to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Connect your GitHub account and select the repository.
4.  Deploy! The `packages.txt` file will automatically install `espeak-ng` which is required for Piper.

## Note on Local Testing (Windows)

The `piper-tts` library is primarily optimized for Linux. On Windows, you may encounter `ImportError: cannot import name 'espeakbridge'` because the required C++ extensions are often missing or require Visual Studio Build Tools to compile during installation.

**If you see this error locally, please proceed to deploy to Streamlit Cloud**, where the Linux environment (and `packages.txt`) ensures everything works correctly.
