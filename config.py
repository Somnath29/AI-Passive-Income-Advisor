import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_OUTPUT_TOKENS = 1024

APP_TITLE = "💰 AI Passive Income Advisor"
APP_SUBTITLE = "Personalized investment recommendations powered by AI"

RISK_LEVELS = ["Low", "Medium", "High"]

TIME_HORIZONS = [
    "Less than 1 year",
    "1–3 years",
    "3–5 years",
    "5–10 years",
    "10+ years"
]

INVESTMENT_GOALS = [
    "Capital Safety (protect my money)",
    "Regular Income (monthly/quarterly returns)",
    "Wealth Growth (long-term growth)",
    "Retirement Planning",
    "Emergency Fund Building"
]