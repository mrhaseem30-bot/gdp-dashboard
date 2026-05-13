from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def get_macro_context(symbol):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""Current global & macro situation for {symbol} analyze karo. 
    Wars, Fed, elections, risk on/off, whale activity — short summary do."""
    
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=400
    )
    return resp.choices[0].message.content
