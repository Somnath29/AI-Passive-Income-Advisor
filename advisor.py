# advisor.py
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"


# ── SMART DOMAIN CHECK ──
def is_finance_related(question: str) -> bool:
    question = question.lower()

    finance_keywords = [
        "invest", "investment", "money", "income", "sip",
        "mutual fund", "stock", "crypto", "etf", "fd",
        "bond", "returns", "portfolio", "risk", "finance",
        "dividend", "wealth", "saving", "rupees", "₹",
        "budget", "profit", "loss", "earn",
        "return", "safe", "growth"
    ]

    # ✅ keyword match
    if any(word in question for word in finance_keywords):
        return True

    # ❌ REMOVED digit logic (IMPORTANT)

    return False


# ── ZERO BUDGET CHECK ──
def is_zero_budget(prompt: str) -> bool:
    prompt = prompt.lower()

    zero_patterns = [
        "₹0",
        "0 rupees",
        "zero rupees",
        "budget is 0",
        "i have 0",
        "i have zero"
    ]

    return any(p in prompt for p in zero_patterns)


# ── MAIN FUNCTION ──
def get_recommendation(prompt, history=None):

    # ✅ STRICT DOMAIN BLOCK (FIRST PRIORITY)
    if not is_finance_related(prompt):
        return """⚠️ I only answer finance-related questions.
                    Please ask about:
                        • Investments  
                        • Passive income  
                        • Financial planning  
                        • Wealth building 😊"""

    # ✅ ZERO BUDGET CHECK
    if is_zero_budget(prompt):
        return """💡 Starting from Zero Budget

You currently don't have investment capital, but here's what you can do:

1. Start Saving Small  
   Save even ₹500–₹1000 per month  

2. Build Emergency Fund  
   Save 3–6 months of expenses  

3. Increase Income  
   Focus on skills / freelancing  

4. Learn Investing Basics  

👉 Your best investment right now is increasing your income."""

    # ── SAFE HISTORY HANDLING ──
    if history is None:
        history = []

    # ── GROQ API CALL ──
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history + [{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


def test_connection():
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Say API connection successful only."}],
            max_tokens=20
        )
        print("✅ API Test:", response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("🔍 Testing Groq API connection...")
    test_connection()