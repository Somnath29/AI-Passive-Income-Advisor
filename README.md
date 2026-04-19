# 💰 AI Passive Income Advisor

Domain-specific **Generative AI chatbot** that provides personalized passive income & investment recommendations.

---

## 🚀 Features
- Personalized investment suggestions  
- Risk-based planning (Low / Medium / High)  
- Time-horizon based recommendations  
- Finance-only AI (rejects unrelated queries)  
- Follow-up conversational support  

---

## 🧠 Problem Solved
- Confusion in choosing investments  
- Lack of financial knowledge  
- No personalized guidance  

👉 Solution: AI-based financial advisor

---

## ⚙️ Tech Stack
- **Frontend**: Streamlit  
- **Backend**: Python  
- **AI Model**: Groq (LLaMA 3.1 8B)  
- **API**: REST API  

---

## 🔄 How It Works
1. User enters financial profile  
2. Prompt is generated  
3. Sent to LLM via API  
4. AI returns recommendation  
5. Displayed in UI  

---

## 🧪 Example Queries
- “Invest ₹50,000 with medium risk”  
- “Compare FD and Mutual Funds”  
- “How to build passive income?”  

---

## 🚫 Domain Restriction
Input: What is 9*7?
Output: ⚠️ I only answer finance-related questions.



---

## ▶️ Run Locally
bash
git clone https://github.com/YOUR_USERNAME/AI-Passive-Income-Advisor.git
cd AI-Passive-Income-Advisor
pip install -r requirements.txt
streamlit run app.py


📂 Structure
app.py
advisor.py
prompt_builder.py
financial_logic.py
config.py


⚠️ Disclaimer

AI-based suggestions only. Do your own research before investing
