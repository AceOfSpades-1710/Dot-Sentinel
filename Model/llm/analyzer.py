import os
import google.generativeai as genai
from llm.prompts import SYSTEM_PROMPT, build_user_prompt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemma-3-1b-it")

def analyze_campaign(summary):
    prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(summary)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 512
        }
    )

    return response.text
