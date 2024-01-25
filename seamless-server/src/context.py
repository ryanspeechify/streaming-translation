import requests
import json
from threading import Thread
from src.logging import initialize_logger
import os

# TODO get language key
prompt = """
Transcription: "[TRANSCRIPT]"
Task: Give a concise, 1-sentence summary of what the speaker is talking about. 
IMPORTANT: The summary must be in the language: [LANGUAGE].
Return the response in JSON format with the following attribute: summary
Response in JSON Format:
"""


logger = initialize_logger(__name__)


class ContextManager:
    def __init__(self):
        self.text_buffer = ""
        self.amt = 0
        self.max_char_memory = 300
        self.char_between_release = 200
        self.language = None
        self.current_context = {}

    def get_current_context(self):
        if self.current_context and self.current_context["read"] is False:
            self.current_context["read"] = True
            return self.current_context["text"]
        return None

    def summarize(self, text):
        if self.language is None:
            return
        try:
            url = "https://voice-llm.openai.azure.com/openai/deployments/voice-LLM/chat/completions?api-version=2023-12-01-preview"
            headers = {
                "Content-Type": "application/json",
                "api-key": os.getenv("AZURE_API_KEY"),
            }

            body = {
                "model": "gpt-35-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt.replace("[TRANSCRIPT]", text).replace(
                            "[LANGUAGE]", self.language
                        ),
                    }
                ],
            }

            response = requests.post(url, headers=headers, json=body)
            response_data = response.json()
            parsed = json.loads(response_data["choices"][0]["message"]["content"])[
                "summary"
            ]
            self.current_context = {"text": parsed, "read": False}
        except Exception as e:
            logger.warning(e)

    def add_text_chunk(self, text):
        self.text_buffer += " " + text
        cur_len = len(self.text_buffer)

        # continously trim context to save memory
        if len(self.text_buffer) > self.max_char_memory:
            self.text_buffer = self.text_buffer[cur_len - self.max_char_memory :]

        self.amt += len(text)
        if self.amt > self.char_between_release:
            self.amt = 0
            thread = Thread(target=self.summarize, args=(self.text_buffer,))
            thread.start()

    def set_language(self, lang):
        self.language = lang
        self.text_buffer = ""
        self.amt = 0
