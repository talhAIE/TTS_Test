import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Path: {sys.path}")

try:
    import piper
    print(f" piper module: {piper}")
    print(f" piper file: {getattr(piper, '__file__', 'no file')}")
except ImportError as e:
    print(f"Failed to import piper: {e}")

try:
    from piper.voice import PiperVoice
    print("Succesfully imported PiperVoice from piper.voice")
except ImportError as e:
    print(f"Failed to import from piper.voice: {e}")

try:
    from piper import PiperVoice
    print("Succesfully imported PiperVoice from piper")
except ImportError as e:
    print(f"Failed to import from piper: {e}")
