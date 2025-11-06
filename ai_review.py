import google.generativeai as genai

genai.configure(api_key='AIzaSyAPduJXu-kY9L0U7YE85LsqBg45RPqXyS0')

model= genai.GenerativeModel('gemini-2.5-flash')

def ai_commentry(symbol, score_dict):
    reasons= "\n".join([f"- {r}" for r in score_dict['reasons']])

    prompt = f"""
you are a CFA level investment analyst .
generate a short investment commentary.
Stock: {symbol}
Verdict: {score_dict['verdict']}
Score: {score_dict['score']}

Reasons:
{reasons}

Task:
Write a professional investment summary (3-4 lines).
Avoid generic sentences. Use fundamental tone.

    """
    res= model.generate_content(prompt)
    return res.text
