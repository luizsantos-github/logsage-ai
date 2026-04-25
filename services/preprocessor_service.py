import os
from collections import deque
from dotenv import load_dotenv

load_dotenv()

class LogPreprocessorService:
    """
    Responsible for sanitizing logs and extracting only
    relevant lines + surrounding context.
    """

    def __init__(self):
        self.include_keywords = self._load_keywords("LOG_INCLUDE_KEYWORDS")
        self.exclude_keywords = self._load_keywords("LOG_EXCLUDE_KEYWORDS")
        self.context_before = int(os.getenv("LOG_CONTEXT_BEFORE", 3))
        self.context_after = int(os.getenv("LOG_CONTEXT_AFTER", 3))
        self.max_lines = int(os.getenv("LOG_MAX_LINES", 200))

    def preprocess(self, log_content: str) -> str:
        """
        Keep:
        - Relevant lines (ERROR, EXCEPTION, etc.)
        - N lines BEFORE match
        - N lines AFTER match
        """

        lines = log_content.splitlines()
        cleaned_lines = []
        previous_lines = deque(maxlen=self.context_before)

        keep_next = 0

        for raw_line in lines:
            line = raw_line.strip()

            if not line:
                continue

            upper = line.upper()

            # Skip noisy lines
            if self._contains_keyword(upper, self.exclude_keywords):
                continue

            # Relevant line found
            if self._contains_keyword(upper, self.include_keywords):

                # include previous context lines
                cleaned_lines.extend(previous_lines)

                # include matched line
                cleaned_lines.append(line)

                # include next lines after match
                keep_next = self.context_after

            elif keep_next > 0:
                cleaned_lines.append(line)
                keep_next -= 1

            # track rolling previous lines
            previous_lines.append(line)

        # Remove duplicates while preserving order
        unique_lines = self._deduplicate(cleaned_lines)

        # Limit payload size
        preprocessed_lines = "\n".join(unique_lines[:self.max_lines])
        return preprocessed_lines

    def _load_keywords(self, env_key: str) -> list[str]:
        value = os.getenv(env_key, "")
        return [
            keyword.strip().upper()
            for keyword in value.split(",")
            if keyword.strip()
        ]

    def _contains_keyword(self, line: str, keywords: list[str]) -> bool:
        return any(keyword in line for keyword in keywords)

    def _deduplicate(self, lines: list[str]) -> list[str]:
        seen = set()
        result = []

        for line in lines:
            if line not in seen:
                result.append(line)
                seen.add(line)

        return result