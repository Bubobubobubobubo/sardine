import subprocess
import sys

try:
    import rtmidi
except ImportError:
    subprocess.check_call([
        sys.executable,
        "-m", "pip", "install", "python-rtmidi"])