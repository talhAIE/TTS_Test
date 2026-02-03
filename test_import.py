try:
    import piper
    print(f"piper module found at: {piper.__file__}")
    from piper import PiperVoice
    print("PiperVoice imported successfully")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
