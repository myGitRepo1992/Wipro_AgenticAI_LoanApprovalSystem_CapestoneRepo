import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))

MODEL = "claude-sonnet-4-6"

APPLICANT_DB_URL = "http://localhost:8001"
RISK_RULES_DB_URL = "http://localhost:8002"
DECISION_SYNTHESIS_URL = "http://localhost:8003"
NOTIFICATION_SYSTEM_URL = "http://localhost:8004"
