from groq import Groq
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def self_improve_code(current_code, error_log="", feedback=""):
    prompt = f"""
    Tum ek expert Python + Trading System Developer ho.
    Current code yeh hai:
    {current_code[:8000]}

    Errors: {error_log}
    User Feedback: {feedback}

    Is code ko better banao:
    - Zyada intelligent decision logic
    - Better early warning
    - Self learning capability
    - Clean + Fast code
    - Error handling strong
    
    Sirf improved complete code do, explanation nahi.
    """

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )
    
    return resp.choices[0].message.content
