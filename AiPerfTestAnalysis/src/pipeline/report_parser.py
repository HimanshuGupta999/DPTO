import json
from pathlib import Path
from src.utils.templates import REPORT_ANALYSIS_PROMPT, ANALYSIS_RESPONSE_FORMAT
import os
from google import genai
from google.genai import types
import pandas as pd

class ReportParser:
    def __init__(self,
                 test_and_infra_details: dict,
                 summary_file_path: str,
                 jmeter_log_paths: list,
                 context_file_path: str,
                 test_feature: str):
        self.test_and_infra_info: dict = test_and_infra_details
        self.summary_file_path: Path = Path(summary_file_path)
        self.summary_file_path: Path = Path(summary_file_path)
        self.jmeter_log_paths: list = [Path(p) for p in jmeter_log_paths]
        self.context_file_path: Path = Path(context_file_path)
        self.test_feature: str = test_feature
        self.queries = test_and_infra_details["questions"]
        self.api = os.environ.get("GEMINI_API_KEY")
        self.model = os.environ.get("GEMINI_MODEL_ID")
        self.summary: dict | None = None
        self.jmeter_logs: str | None = None
        self.context: dict | None = None

    def extract_metrics(self) -> dict:
        """
        Extracts the performance summary from the provided summary file.
        """
        if not self.summary_file_path.exists():
            raise FileNotFoundError(f"Summary file not found at: {self.summary_file_path}")

        try:
            with self.summary_file_path.open('r') as file:
                data = json.load(file)
                return data.get("Total", {})
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in summary file: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while reading summary file: {e}")

    def read_jmeter_log(self) -> str:
        """
        Reads multiple JMeter log files and returns concatenated filtered logs.
        Each section is prefixed with the log filename for better clarity.
        """
        all_logs = []
        for log_path in self.jmeter_log_paths:
            if not log_path.exists():
                raise FileNotFoundError(f"JMeter log file not found at: {log_path}")

            try:
                with log_path.open('r') as file:
                    lines = file.readlines()
                    important_lines = [line.strip() for line in lines if "WARN" in line or "ERROR" in line]

                    if important_lines:
                        all_logs.append(f"\n--- Log from file: {log_path.name} ---")
                        all_logs.extend(important_lines)
            except Exception as e:
                raise RuntimeError(f"Error reading JMeter log file {log_path}: {e}")

        # Limit total log lines to 100 for token efficiency
        return "\n".join(all_logs)

    def generate_analysis_prompt(self) -> str:
        """
        Formats the prompt to be passed to the LLM.
        Includes summary data, JMeter logs, and test/infrastructure details.
        """
        return REPORT_ANALYSIS_PROMPT.format(
            SUMMARY=self.summary,
            JMETER_LOGS=self.jmeter_logs,
            TEST_AND_INFRA_DETAILS=self.test_and_infra_info,
            ANALYSIS_RESPONSE_FORMAT=ANALYSIS_RESPONSE_FORMAT,
            CUSTOM_QUESTIONS=self.queries,
            CONTEXT_DATA=self.context,
            TEST_FEATURE=self.test_feature
        )

    def gemini_analysis(self, input_content):
        """
        Sends the prompt to the Gemini LLM and returns the generated content.
        """
        client = genai.Client(api_key=self.api)
        response = client.models.generate_content(
            model=self.model,
            contents=[input_content],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if hasattr(response, "status_code") and response.status_code != 200:
            raise RuntimeError(f"Model call failed with status code {response.status_code}")

        return response.text

    def read_context(self, context_file_path):
        try:
            context_df = pd.read_csv(context_file_path, dtype=str)
            context_df = context_df.astype(str)
            return context_df.to_dict(orient="records")
        except FileNotFoundError:
            raise FileNotFoundError(f"Context file not found at: {context_file_path}")
        except pd.errors.EmptyDataError:
            raise RuntimeError(f"Context file is empty: {context_file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading context file {context_file_path}: {e}")

    def get_analysis(self) -> dict:
        """
        Retrieves AI-generated recommendations based on report summary and infra details.
        """
        self.summary = self.extract_metrics()
        self.jmeter_logs = self.read_jmeter_log()
        self.context = self.read_context(context_file_path=self.context_file_path)
        prompt_content = self.generate_analysis_prompt()

        raw_response = self.gemini_analysis(input_content=prompt_content)

        try:
            parsed_response = json.loads(raw_response)

        except json.JSONDecodeError:
            parsed_response = {
                "error": "Failed to parse LLM response into JSON.",
                "raw_response": raw_response
            }

        return {
            "recommendation": parsed_response
        }
