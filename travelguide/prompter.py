"""
Prompt module to access LLM API

A simple prompting module with a base interface and an OpenAI implementation.
"""

from abc import ABC, abstractmethod
# import ast
from dotenv import load_dotenv
import json
import os
import pprint
import re
import traceback
# import logging

# LLM API
from google import genai  # Google Gemini
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, Modality

# import openai  # OpenAI ChatGPT

# JSON schema
import json
from jsonschema import Draft7Validator, exceptions


# Configure basic logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class BasePrompter(ABC):
    """
    Abstract base class defining the interface for prompters.

    All subclasses must implement the prompt() method.
    """

    @abstractmethod
    def prompt(self, prompt_text: str) -> str:
        """
        Send a prompt to the API and return the response as a string.

        Args:
            prompt_text (str): The input prompt to send.

        Returns:
            str: The API-generated response.

        Raises:
            Exception: Any exception that occurs during the prompt operation.
        """
        pass


class GenAIPrompter(BasePrompter):
    """
    Concrete implementation of BasePrompter for interacting with the
    GenAI API from Google.

    Implementing BasePrompter.
    """

    def __init__(self, input_prompts: dict):
        """
        Initialize the OpenAIPrompter by setting the OpenAI API key.

        Raises an error if the API key is missing or invalid.
        """
        self.input_prompts = input_prompts

        load_dotenv()
        api_key = os.getenv('GENAI_API_KEY')

        if not api_key:
            raise ValueError(
                "Invalid or missing Google GenAI API key. Please set "
                "GENAI_API_KEY correctly in .env.")

        # Initialize the client
        self.client = genai.Client(api_key=api_key)

    def prompt(self, prompt_text: str, json_schema: str) -> dict:
        """
        Send a prompt to Google's ChatCompletion API and returns the response.

        Args:
            prompt_text (str): The prompt text to send.

        Returns:
            str: The generated response from the API.

        Raises:
            RuntimeError: If the API request fails.
        """
        try:
            # logger.info("Sending prompt to GenAI...")

            # print(genai.__version__)

            # model_id = "gemini-2.0-flash"
            # model_id = "gemini-2.5-pro-exp-03-25",
            # model_id = "gemini-2.5-flash-preview-04-17"
            model_id = "gemini-2.5-flash-preview-05-20"

            # https://ai.google.dev/gemini-api/docs/grounding?lang=python
            google_search_tool = Tool(
                google_search=GoogleSearch()
            )
            response = self.client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=GenerateContentConfig(
                    tools=[google_search_tool],
                    # response_modalities=["TEXT"],
                    response_modalities=[Modality.TEXT],
                    # temperature=0.6, # error
                    # temperature=0.8,  # ok
                    temperature=1,  # ok
                    # temperature=1.5,  # ok
                )
            )

            # https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-preview
            # response = self.client.models.generate_content(
            #     # model="gemini-2.0-flash",
            #     # model="gemini-2.5-pro-exp-03-25",
            #     model="gemini-2.5-flash-preview-04-17",
            #     contents=prompt_text,
            # )
            if (response.text is None):
                print(type(response))
                print(response)
                result = ""
            else:
                # print(type(response.text))
                # print(response.text)
                result = self.extract_dict_from_response(response.text,
                                                         json_schema)

            # logger.info("Received response from GenAI.")
            return result
        except ValueError as e:
            # logger.error(f"Value error: {e}")
            traceback.print_exc()
            raise ValueError(f"Value error: {e}")
        except Exception as e:
            # logger.error(f"Unexpected error: {e}")
            traceback.print_exc()
            raise RuntimeError(f"GenAI API request failed: {e}") from e

    def prompt_for_json(self, prompt_text: str, json_schema: str) -> dict:
        """
        Send a prompt to Google's ChatCompletion API and returns the response.

        Args:
            prompt_text (str): The prompt text to send.
            json_schema (str): Google's GenAI API expects a simpler "type-
                      enforced schema" (Google's own custom Schema format).

        Returns:
            str: The generated response from the API.

        Raises:
            RuntimeError: If the API request fails.
        """
        try:
            # logger.info("Sending prompt to GenAI...")

            # Validate JSON schema as JSON and convert it to dict
            json_schema_dict = json.loads(json_schema)
            # print("✅ JSON Schema string is valid and loaded successfully.")

            # Validate JSON schema as JSON schema
            Draft7Validator.check_schema(json_schema_dict)
            # print("✅ Schema is a valid JSON Schema (Draft 7).")

            # Prompt LLM API
            # print(genai.__version__)

            # model_id = "gemini-2.0-flash"
            # model_id="gemini-2.5-pro-exp-03-25",
            model_id = "gemini-2.5-flash-preview-04-17"

            response = self.client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=GenerateContentConfig(
                    response_modalities=[Modality.TEXT],
                    temperature=1,  # ok
                    response_mime_type="application/json",
                    response_schema=json_schema_dict,
                )
            )

            if (response.text is None):
                print(type(response))
                print(response)
                result = ""
            else:
                # print(type(response.text))
                # print(response.text)
                try:
                    result = json.loads(response.text)
                    print("✅ Converted JSON is valid.")
                except json.JSONDecodeError as e:
                    print("❌ Converted JSON is invalid: {e}")
                    print("\n=== JSON Draft (before conversion) ===\n")
                    print(prompt_text)
                    print("\n=== JSON (after conversion) ===\n")
                    print(response.text)
                    # Log to ease debugging
                    pp = pprint.PrettyPrinter(indent=2, width=120)
                    with open('debug/error_json_draft_'
                              '.txt', 'w', encoding='utf-8') as f:
                        f.write(pp.pformat(prompt_text))
                    with open('debug/error_json_converted_'
                              '.json', 'w', encoding='utf-8') as f:
                        f.write(pp.pformat(response.text))
                    result = ""

            # logger.info("Received response from GenAI.")
            return result
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON Schema string: {e}")
        except exceptions.SchemaError as e:
            print(f"❌ Schema is invalid: {e}")
        except ValueError as e:
            # logger.error(f"Value error: {e}")
            traceback.print_exc()
            raise ValueError(f"Value error: {e}")
        except Exception as e:
            # logger.error(f"Unexpected error: {e}")
            traceback.print_exc()
            raise RuntimeError(f"GenAI API request failed: {e}") from e

    # @staticmethod
    def extract_dict_from_response(self, response_str: str, json_schema: str
                                   ) -> dict:
        """
        Extract and parse a Python dict embedded in a string response.

        Args:
            response_str (str): The raw string containing the dict.

        Returns:
            dict: Parsed dictionary object.

        Raises:
            ValueError: If parsing fails.
        """
        try:
            clean_str = response_str.strip()

            # Remove code fences like ```json or ```python
            # clean_str = clean_str.removeprefix(
            #    '```python').removesuffix('```').strip()
            # clean_str = clean_str.removeprefix(
            #    '```json').removesuffix('```').strip()
            clean_str = re.sub(r'```(json|python)?', '',
                               clean_str, flags=re.IGNORECASE).strip()

            # Remove illegal control characters: replace raw control chars
            # with safe space
            # (except for \n and \t which are often fine outside JSON strings)
            # clean_str = re.sub(r'[\x00-\x1F\x7F]', ' ', clean_str)
            clean_str = re.sub(
                r'[\x00-\x09\x0B-\x0C\x0E-\x1F\x7F]', ' ', clean_str)

            # Additional comments after the JSON => Keep only the first valid
            # JSON object
            # Find the first JSON object using a simple brace count
            # brace_count = 0
            # end_idx = None
            # for i, char in enumerate(clean_str):
            #     if char == '{':
            #         brace_count += 1
            #     elif char == '}':
            #         brace_count -= 1
            #         if brace_count == 0:
            #             end_idx = i + 1
            #             break

            # Find first '{'
            first_brace_idx = clean_str.find('{')
            if first_brace_idx == -1:
                raise ValueError(
                    "No JSON object found in response (no opening brace).")

            json_candidate = clean_str[first_brace_idx:]

            # Brace matching to find end of JSON object
            brace_count = 0
            end_idx = None
            for i, char in enumerate(json_candidate):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break

            if end_idx is None:
                raise ValueError("No complete JSON object found in response"
                                 " (unbalanced braces).")
                # raise ValueError("No complete JSON object found in response.")

            clean_str = clean_str[:end_idx].strip()
            # print("***cleanded response")
            # print(clean_str)

            clean_str = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', clean_str)
            # print("***removed citation markers")
            # print(clean_str)

            # return ast.literal_eval(clean_str)
            return json.loads(clean_str)
        except json.JSONDecodeError as e:

            try:
                if (json_schema is not None):
                    # Try to convert JSON with LLM API
                    print("*****JSON is not valid - try to convert JSON with"
                          " LLM API")
                    convert_prompt_text = self.input_prompts[
                        "general_json_conversion_instructions"] + clean_str
                    print("*****Converted JSON")
                    print(convert_prompt_text)
                    json_response = self.prompt(convert_prompt_text,
                                                json_schema)
                    print(json_response)
                    return json_response
                else:
                    print("\n=== JSON Schema is None ===\n")

            except Exception:
                print("\n=== Raw Response for Debugging ===\n")
                print(response_str)
                # print("\n=== Cleaned Response ===\n")
                # print(clean_str)

                # Log to ease debugging
                pp = pprint.PrettyPrinter(indent=2, width=120)
                with open('debug/error_prompt_response_'
                          '.txt', 'w', encoding='utf-8') as f:
                    f.write(pp.pformat(response_str))
                # with open('debug/error_prompt_response_'
                #           '.json', 'w', encoding='utf-8') as f:
                #     f.write(pp.pformat(clean_str))

                traceback.print_exc()
                raise ValueError(
                    f"Failed to parse response into dict (JSON error): {e}")

        except Exception as e:
            traceback.print_exc()
            raise ValueError(f"Failed to parse response into dict: {e}")


# class OpenAIPrompter(BasePrompter):
#     """
#     Concrete implementation of BasePrompter for interacting with the
#     OpenAI API.

#     Implementing BasePrompter.
#     """

#     def __init__(self):
#         """
#         Initialize the OpenAIPrompter by setting the OpenAI API key.

#         Raises an error if the API key is missing or invalid.
#         """
#         load_dotenv()
#         api_key = os.getenv('OPENAI_API_KEY')

#         if not api_key or not api_key.startswith("sk-"):
#             raise ValueError(
#                 "Invalid or missing OpenAI API key. Please set "
#                 "OPENAI_API_KEY correctly in .env.")

#         # Initialize the OpenAI client
#         self.client = openai.OpenAI(api_key=api_key)

#     def prompt(self, prompt_text: str) -> str:
#         """
#         Send a prompt to OpenAI's ChatCompletion API and returns the response.

#         Args:
#             prompt_text (str): The prompt text to send.

#         Returns:
#             str: The generated response from the API.

#         Raises:
#             RuntimeError: If the API request fails.
#         """
#         try:
#             # logger.info("Sending prompt to OpenAI...")
#             response = openai.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=[{"role": "user", "content": prompt_text}]
#             )
#             result = response.choices[0].message.content.strip()
#             # logger.info("Received response from OpenAI.")
#             return result
#         except openai.error.OpenAIError as e:
#             # logger.error(f"OpenAI API error: {e}")
#             raise RuntimeError(f"OpenAI API error: {e}")
#         except Exception as e:
#             # logger.error(f"Unexpected error: {e}")
#             raise RuntimeError(f"OpenAI API request failed: {e}") from e
