from dotenv import load_dotenv
from pathlib import Path

def start_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
