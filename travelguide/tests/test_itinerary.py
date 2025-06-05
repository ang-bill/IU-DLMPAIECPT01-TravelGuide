
import unittest
import ast
import os
import pprint
from itinerary import Itinerary
from input_loader import load_input_prompt_files


class TestItinerary(unittest.TestCase):
    def test_generate_itinerary_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        result = i.generate_itinerary_prompt()
        self.assertIn('travel itinerary', result)

    def test_call_api_itinerary_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        prompt = i.generate_itinerary_prompt()
        result = i.call_api_itinerary_prompt(prompt)
        # print(result)
        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_itinerary_01.txt', 'w', encoding='utf-8') as f:
            f.write(pp.pformat(result))
        self.assertIsInstance(result, dict,
                              "Response should be a string")
        self.assertGreater(len(result), 0,
                           "Response should not be empty")
        self.assertIn('history_destination', result)
        self.assertIn('itinerary', result)

    def test_create_itinerary(self):
        input_prompts = load_input_prompt_files("../prompts")
        # i = Itinerary()
        # str_i = {"itinerary": "Itinerary generated from: "}
        # result = i.create_itinerary(str_i)
        # self.assertIn('Itinerary', result)
        i = Itinerary(input_prompts)
        # prompt = i.generate_itinerary_prompt(
        #     load_input_prompt_files("../prompts"))
        # itinerary_data = i.call_api_itinerary_prompt(prompt)
        # print(itinerary_data)
        with open("testfiles/test_itinerary_02.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()

        itinerary_data = ast.literal_eval(str_itinerary_data)
        htmlsource = i.create_itinerary(itinerary_data,
                                        os.path.join(os.path.dirname(__file__),
                                                     '..', 'templates'),
                                        os.path.join(os.path.dirname(__file__),
                                                     '..', 'outputs'))
        self.assertIsInstance(htmlsource, str,
                              "HTML source should be a string")
        self.assertGreater(len(htmlsource), 0,
                           "HTML source should not be empty")
        self.assertIn('Route Description', htmlsource)

    def test_retrieve_all_pois(self):
        input_prompts = load_input_prompt_files("../prompts")
        # i = Itinerary()
        # str_i = {"itinerary": "Itinerary generated from: "}
        # result = i.create_itinerary(str_i)
        # self.assertIn('Itinerary', result)
        i = Itinerary(input_prompts)
        # prompt = i.generate_itinerary_prompt(
        #     load_input_prompt_files("../prompts"))
        # itinerary_data = i.call_api_itinerary_prompt(prompt)
        # with open("testfiles/test_itinerary_03.txt", 'r', encoding='utf-8') as file:
        #     str_itinerary_data = file.read()
        with open("testfiles/test_itinerary_02.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)
        self.assertIsInstance(all_pois, dict,
                              "POI list should be a dict")
        self.assertGreater(len(all_pois), 0,
                           "POI list should not be empty")
        self.assertIn('POI-01', all_pois)


if __name__ == "__main__":
    # Run the test
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestItinerary('test_generate_itinerary_prompt'))
    # suite.addTest(TestItinerary('test_call_api_itinerary_prompt'))
    # suite.addTest(TestItinerary('test_create_itinerary'))
    suite.addTest(TestItinerary('test_retrieve_all_pois'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
