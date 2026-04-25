from openai import OpenAI
import json
from schemas.log_analyzer_response import LogAnalyzerResponse

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

Log to analyze: 
"""

class LogService:

    def __init__(self, ai_client: OpenAI):
        self.ai_client = ai_client

    async def process_uploaded_log(self, file):
        """ Preprocess and analyze the uploaded log file """
        # Read the file

        # Preprocess

        # Call AI

        return None

    def analyze_log(self, log_content: str):
        return self.call_openai(log_content)

    def call_openai(self, log_content: str):
        """ Calls the OpenAI library to analyze the log """

        prompt = f"{PROMPT}{log_content}"

        response = self.ai_client.responses.create(
            model="gpt-5.4",
            instructions=INSTRUCTIONS,
            input = prompt,
        )

        try:
            # How to parse raw JSON from LLM
            data = json.loads(response.output_text)
            return LogAnalyzerResponse(**data)

        except json.JSONDecodeError:
            raise ValueError("AI returned invalid JSON")

        except Exception as e:
            raise ValueError(f"Failed to parse AI response: {e}")
