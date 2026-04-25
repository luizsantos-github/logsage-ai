from openai import OpenAI
import json
from schemas.log_analyzer_response import LogAnalyzerResponse
from services.preprocessor_service import LogPreprocessorService

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
        self.preprocessor = LogPreprocessorService()

    async def process_uploaded_log(self, file):
        """ Preprocess and analyze the uploaded log file """
        # Read the file
        content = await file.read()
        raw_log = content.decode("utf-8", errors="ignore")

        # Call preprocessor
        clean_log = self.preprocessor.preprocess(raw_log)

        # Call AI
        return self._call_openai(clean_log)

    def analyze_log(self, log_content: str):
        return self._call_openai(log_content)

    def _call_openai(self, log_content: str):
        """ Calls the OpenAI library to analyze the log """

        prompt = f"{PROMPT}{log_content}"

        response = self.ai_client.responses.create(
            model="gpt-5.4",
            instructions=INSTRUCTIONS,
            input = prompt,
        )

        try:
            # How to parse raw JSON from LM to a pydantic model. used (**data)
            data = json.loads(response.output_text)
            return LogAnalyzerResponse(**data)

        except json.JSONDecodeError:
            raise ValueError("AI returned invalid JSON")

        except Exception as e:
            raise ValueError(f"Failed to parse AI response: {e}")
