from pathlib import Path

def load_key():
    key_path = Path(__file__).parent.parent / "private" / "api_key.txt"
    return key_path.read_text().strip()
