import os
from pathlib import Path

def load_key() -> str:
    key_path = os.environ.get("API_KEY_PATH")

    if not key_path:
        raise RuntimeError("API_KEY_PATH environment variable not set")

    path = Path(key_path)

    if not path.exists():
        raise RuntimeError(f"API key file not found at {path}")

    return path.read_text().strip()
