# financial_logic.py
# Rule-based financial logic layer
# This runs BEFORE the AI — filters investments based on hard rules

INVESTMENT_DATA = {
    "Fixed Deposit (FD)": {
        "risk": "Low",
        "min_investment": 1000,
        "returns": "6–7% per year",
        "horizon": ["Less than 1 year", "1–3 years", "3–5 years"],
        "description": "Bank-backed deposit with guaranteed returns"
    },
    "Recurring Deposit (RD)": {
        "risk": "Low",
        "min_investment": 500,
        "returns": "5–6% per year",
        "horizon": ["Less than 1 year", "1–3 years"],
        "description": "Monthly savings with fixed interest"
    },
    "Government Bonds": {
        "risk": "Low",
        "min_investment": 10000,
        "returns": "7–8% per year",
        "horizon": ["3–5 years", "5–10 years", "10+ years"],
        "description": "Sovereign-backed securities, very safe"
    },
    "Index Funds / ETFs": {
        "risk": "Medium",
        "min_investment": 500,
        "returns": "10–12% per year",
        "horizon": ["3–5 years", "5–10 years", "10+ years"],
        "description": "Diversified market funds tracking indices like Nifty 50"
    },
    "Dividend Stocks": {
        "risk": "Medium",
        "min_investment": 5000,
        "returns": "8–14% per year",
        "horizon": ["3–5 years", "5–10 years"],
        "description": "Stocks that pay regular dividends"
    },
    "REITs": {
        "risk": "Medium",
        "min_investment": 10000,
        "returns": "8–10% per year",
        "horizon": ["3–5 years", "5–10 years"],
        "description": "Real estate investment without buying property"
    },
    "P2P Lending": {
        "risk": "High",
        "min_investment": 50000,
        "returns": "12–18% per year",
        "horizon": ["1–3 years", "3–5 years"],
        "description": "Lending money to individuals via platforms"
    },
    "Cryptocurrency": {
        "risk": "High",
        "min_investment": 500,
        "returns": "Very variable (can be negative)",
        "horizon": ["3–5 years", "5–10 years"],
        "description": "Digital assets — high risk, high reward"
    },
    "Small-Cap Stocks": {
        "risk": "High",
        "min_investment": 5000,
        "returns": "15–25% (or losses)",
        "horizon": ["5–10 years", "10+ years"],
        "description": "High growth potential companies, very volatile"
    }
}


def get_eligible_investments(budget: float, risk: str, horizon: str) -> list:
    """
    Filters investments based on budget, risk level, and time horizon.
    Returns list of eligible investment names.
    """
    eligible = []

    for name, data in INVESTMENT_DATA.items():
        # Check risk level matches
        risk_match = (
            data["risk"] == risk or
            (risk == "High" and data["risk"] in ["Low", "Medium", "High"]) or
            (risk == "Medium" and data["risk"] in ["Low", "Medium"])
        )

        # Check budget is enough
        budget_match = budget >= data["min_investment"]

        # Check time horizon matches
        horizon_match = horizon in data["horizon"]

        if risk_match and budget_match and horizon_match:
            eligible.append(name)

    return eligible


def get_investment_summary(eligible: list) -> str:
    """
    Returns a formatted string summary of eligible investments.
    Used to inject into the AI prompt.
    """
    if not eligible:
        return "No specific investments matched. Please provide general advice."

    summary = ""
    for name in eligible:
        data = INVESTMENT_DATA[name]
        summary += f"- {name}: {data['returns']} returns, Min ₹{data['min_investment']}, {data['description']}\n"

    return summary


def validate_inputs(budget: float, risk: str, goal: str, horizon: str) -> tuple:
    """
    Validates user inputs before processing.
    Returns (is_valid: bool, error_message: str)
    """
    if budget <= 0:
        return False, "Budget must be greater than ₹0"

    if budget < 500:
        return False, "Minimum budget for any investment is ₹500"

    if risk not in ["Low", "Medium", "High"]:
        return False, "Risk level must be Low, Medium, or High"

    if not goal or len(goal.strip()) < 3:
        return False, "Please describe your financial goal"

    if not horizon:
        return False, "Please select a time horizon"

    return True, ""