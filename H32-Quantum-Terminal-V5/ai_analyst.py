from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_verdict_with_timeframe(symbol, price, structure, score, reasons, macro):
    prompt = f"""
    Tum elite Smart Money Trader ho. 
    {symbol} Price: ${price:,.4f}
    Structure: {structure}
    Confluence: {score}/100
    Reasons: {reasons}
    Macro: {macro}

    Timeframe Analysis + Clear Verdict do:
    - Next 24-72 hours
    - 4-10 days move possible?
    - Best entry window
    - SL aur TP levels
    - Final: STRONG BUY / CAUTIOUS / HOLD
    Urdu + English mix mein short aur clear jawab.
    """
    
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25,
        max_tokens=900
    )
    return response.choices[0].message.content
