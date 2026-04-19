# app.py
# Main Streamlit application
# Run with: streamlit run app.py

import streamlit as st
from advisor import get_recommendation
from prompt_builder import build_initial_prompt, build_followup_prompt
from financial_logic import validate_inputs
from config import (
    APP_TITLE, APP_SUBTITLE,
    RISK_LEVELS, TIME_HORIZONS, INVESTMENT_GOALS
)

# ── Page Configuration ─────────────────────────
st.set_page_config(
    page_title="AI Passive Income Advisor",
    page_icon="💰",
    layout="centered"
)

# ── Custom CSS Styling ─────────────────────────
st.markdown("""
<style>

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    color: white;
}

/* ── Theme Adaptive Cards ── */
.recommendation-box {
    background: var(--secondary-background-color);
    border-left: 4px solid #4caf50;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: var(--text-color);
}

.user-message {
    background: rgba(0, 123, 255, 0.1);
    padding: 0.8rem 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    color: var(--text-color);
}

.ai-message {
    background: rgba(76, 175, 80, 0.1);
    padding: 0.8rem 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 3px solid #4caf50;
    color: var(--text-color);
}

/* ── Profile Card ── */
.profile-card {
    background: var(--secondary-background-color);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    border: 1px solid #f59e0b;
    color: var(--text-color);
}

/* ── Improve text readability ── */
h1, h2, h3, h4, p, div {
    color: var(--text-color);
}

</style>
""", unsafe_allow_html=True)


# ── Initialize Session State (Memory) ─────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "recommendation_given" not in st.session_state:
    st.session_state.recommendation_given = False

if "groq_history" not in st.session_state:
    st.session_state.groq_history = []


# ── Header ─────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>💰 AI Passive Income Advisor</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar — User Profile Form ────────────────
with st.sidebar:
    st.header("📋 Your Financial Profile")
    st.markdown("Fill in your details to get personalized recommendations.")

    budget = st.number_input(
        "💵 Investment Budget (₹)",
        min_value=0,
        max_value=10000000,
        value=50000,
        step=1000,
        help="How much money do you want to invest?"
    )

    risk = st.radio(
        "⚖️ Risk Tolerance",
        options=RISK_LEVELS,
        index=1,
        help="Low = safe, Medium = balanced, High = aggressive"
    )

    goal = st.selectbox(
        "🎯 Financial Goal",
        options=INVESTMENT_GOALS,
        help="What do you want to achieve?"
    )

    horizon = st.selectbox(
        "⏳ Time Horizon",
        options=TIME_HORIZONS,
        index=2,
        help="How long can you keep money invested?"
    )

    st.markdown("---")

    get_advice_btn = st.button(
        "🔍 Get My Recommendations",
        type="primary",
        use_container_width=True
    )

    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.user_profile = {}
        st.session_state.recommendation_given = False
        st.session_state.groq_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ AI Settings")
    st.caption("Temperature: 0.7 (Balanced creativity)")
    st.caption("Top-p: 0.9 (Diverse vocabulary)")
    st.caption("Model: LLaMA 3.1 via Groq")


# ── Main Content Area ──────────────────────────
main_container = st.container()

with main_container:

    # Show user profile card if filled
    if st.session_state.recommendation_given and st.session_state.user_profile:
        profile = st.session_state.user_profile
        st.markdown(f"""
        <div class="profile-card">
            <strong>📊 Active Profile:</strong> 
            Budget ₹{profile.get('budget', 0):,} | 
            Risk: {profile.get('risk', '')} | 
            Goal: {profile.get('goal', '')} | 
            Horizon: {profile.get('horizon', '')}
        </div>
        """, unsafe_allow_html=True)

    # ── Handle Get Recommendations Button ──────
    if get_advice_btn:
        is_valid, error_msg = validate_inputs(budget, risk, goal, horizon)

        if not is_valid:
            st.error(f"⚠️ {error_msg}")
        else:
            # Save user profile to session
            st.session_state.user_profile = {
                "budget": budget,
                "risk": risk,
                "goal": goal,
                "horizon": horizon
            }

            # Build the prompt
            prompt = build_initial_prompt(budget, risk, goal, horizon)

            # Add to chat history display
            user_message = f"I have ₹{budget:,} to invest. Risk level: {risk}. Goal: {goal}. Time horizon: {horizon}."
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_message
            })

            # Call AI
            with st.spinner("🤖 Analyzing your financial profile..."):
                response = get_recommendation(prompt, st.session_state.groq_history)

            # Save to both display history and groq history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })

            # Update groq history for memory
            st.session_state.groq_history.append({
                "role": "user",
                "content": user_message
            })
            st.session_state.groq_history.append({
                "role": "assistant",
                "content": response
            })

            st.session_state.recommendation_given = True
            st.rerun()

    # ── Display Chat History ───────────────────
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 Advisor:</strong><br>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(msg["content"])

        # ── Follow-up Question Input ───────────
        st.markdown("---")
        st.markdown("### 💭 Ask a Follow-up Question")

        followup = st.text_input(
            "Ask anything about your investments...",
            placeholder="e.g. How do I start investing in Index Funds?",
            key="followup_input"
        )

        if st.button("Send →", type="primary"):
            if followup.strip():
                # Build follow-up prompt
                followup_prompt = build_followup_prompt(
                    followup,
                    st.session_state.user_profile
                )

                # Add to display history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": followup
                })

                # Call AI with memory
                with st.spinner("🤖 Thinking..."):
                    response = get_recommendation(
                        followup_prompt,
                        st.session_state.groq_history
                    )

                # Save response
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

                # Update memory
                st.session_state.groq_history.append({
                    "role": "user",
                    "content": followup
                })
                st.session_state.groq_history.append({
                    "role": "assistant",
                    "content": response
                })

                st.rerun()

    else:
        # Welcome screen
        st.markdown("""
        ### 👋 Welcome to AI Passive Income Advisor!

        **How to get started:**
        1. 👈 Fill in your financial profile in the sidebar
        2. Click **"Get My Recommendations"**
        3. Get personalized passive income strategies
        4. Ask follow-up questions to learn more!

        ---

        **What I can help you with:**
        - 🏦 Fixed Deposits & Bonds (Low Risk)
        - 📈 Index Funds & ETFs (Medium Risk)
        - 💹 Stocks & Crypto (High Risk)
        - 🏢 REITs & P2P Lending
        - 📊 Portfolio allocation advice

        > ⚠️ *This is an educational tool. Not certified financial advice.*
        """)


# ── Footer ─────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>💰 AI Passive Income Advisor | Built with Streamlit + LLaMA 3.1 | Academic Project</small></center>",
    unsafe_allow_html=True
)