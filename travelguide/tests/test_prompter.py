
import unittest
from input_loader import load_input_prompt_files
from prompter import GenAIPrompter


class TestPrompter(unittest.TestCase):
    """Simple test class for validating the prompter implementations."""

    def test_genai_prompter(self):
        """
        Test GenAI Prompter.

        Tests the GenAIPrompter by sending a basic prompt and validating the
        response.
        """
        genai_prompter = GenAIPrompter(None)

        try:
            response = genai_prompter.prompt("Hello, who are you?", None)
        except ValueError as e:
            print(e)
            # Assertions
            # self.assertIn('JSON', e)

    # @staticmethod
    # def test_openai_prompter(self):
    #     """
    #     Test OpenAI Prompter.

    #     Tests the OpenAI Prompter by sending a basic prompt and validating the
    #     response.
    #     """
    #     openai_prompter = OpenAIPrompter()
    #     response = openai_prompter.prompt("Hello, who are you?")

    #     # Assertions
    #     self.assertIsInstance(response, str,
    #                           "Response should be a string")
    #     self.assertGreater(len(response.strip()), 0,
    #                        "Response should not be empty")

    def test_genai_prompt_for_json_itinerary(self):
        """
        Test GenAI Prompter.

        Tests the GenAIPrompter by sending a basic prompt and validating the
        response.
        """

        # Load testfile
        with open("testfiles/test_prompt_json_conversion_itinerary_01.txt",
                  'r', encoding='utf-8') as file:
            str_prompt = file.read()
        # print(str_prompt)

        # Load JSON schema
        input_prompts = load_input_prompt_files("../prompts")
        str_schema = input_prompts["itinerary_prompt_output_schema"]
        # print(str_schema)

        genai_prompter = GenAIPrompter(input_prompts)
        response = genai_prompter.prompt_for_json(str_prompt, str_schema)
        # print(type(response))
        # print(response)

        # Assertions
        self.assertIsInstance(response, dict,
                              "Response should be a dict")
        self.assertIn('history_destination', response)

    def test_genai_prompt_for_json_poi(self):
        """
        Test GenAI Prompter.

        Tests the GenAIPrompter by sending a basic prompt and validating the
        response.
        """

        # Load testfile
        with open("testfiles/test_prompt_json_conversion_poi_01.txt", 'r',
                  encoding='utf-8') as file:
            str_prompt = file.read()
        # print(str_prompt)

        # Load JSON schema
        input_prompts = load_input_prompt_files("../prompts")
        str_schema = input_prompts["poi_prompt_output_schema"]
        # print(str_schema)

        genai_prompter = GenAIPrompter(input_prompts)
        response = genai_prompter.prompt_for_json(str_prompt, str_schema)
        # print(type(response))
        # print(response)

        # Assertions
        self.assertIsInstance(response, dict,
                              "Response should be a dict")
        self.assertIn('need_to_know', response)

    def test_genai_prompt_for_json_poi_images(self):
        """
        Test GenAI Prompter.

        Tests the GenAIPrompter by sending a basic prompt and validating the
        response.
        """

        # Load testfile
        with open("testfiles/test_prompt_json_conversion_poi_images_01.txt",
                  'r', encoding='utf-8') as file:
            str_prompt = file.read()
        # print(str_prompt)

        # Load JSON schema
        input_prompts = load_input_prompt_files("../prompts")
        str_schema = input_prompts["poi_images_prompt_output_schema"]
        # print(str_schema)

        genai_prompter = GenAIPrompter(input_prompts)
        response = genai_prompter.prompt_for_json(str_prompt, str_schema)
        # print(type(response))
        # print(response)

        # Assertions
        self.assertIsInstance(response, dict,
                              "Response should be a dict")
        self.assertIn('wikimedia_urls', response)


if __name__ == "__main__":
    # Run the test
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestPrompter('test_genai_prompter'))
    # suite.addTest(TestPrompter('test_genai_prompt_for_json_itinerary'))
    # suite.addTest(TestPrompter('test_genai_prompt_for_json_poi'))
    # suite.addTest(TestPrompter('test_genai_prompt_for_json_poi_images'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
