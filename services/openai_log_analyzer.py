import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSTRUCTIONS = 'You are a senior DevOps incident engineer'

PROMPT = """
Analyze this backend application log.

Return JSON:
{
"summary" : "",
"root_cause" : "",
"severity" : "",
"recommendation" : "
}

Log: 
"""

def analyze_log(log: str):
    input_message = f"{PROMPT}{log}"

    response = ai_client.responses.create(
        model="gpt-5.4",
        instructions=INSTRUCTIONS,
        input = input_message
    )

    return json.loads(response.output_text)