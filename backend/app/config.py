# ============================================================
# config.py — All settings loaded from .env
# ============================================================
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
API_HOST           = os.getenv("API_HOST", "127.0.0.1")
API_PORT           = int(os.getenv("API_PORT", 8000))
MAX_FILE_SIZE_MB   = int(os.getenv("MAX_FILE_SIZE_MB", 50))
ALLOWED_EXTENSIONS = os.getenv(
    "ALLOWED_EXTENSIONS",
    ".pdf,.png,.jpg,.jpeg,.docx,.webp"
).split(",")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
STORAGE_PATH       = os.getenv("STORAGE_PATH", "./storage")