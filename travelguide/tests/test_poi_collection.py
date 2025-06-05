import unittest
import ast
import os
import pprint
from itinerary import Itinerary
from input_loader import load_input_prompt_files
from poi_collection import PoiCollection


class TestPoiCollection(unittest.TestCase):
    def test_generate_poi_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        pc = PoiCollection(input_prompts, all_pois)
        result = pc.create_poi_pages(os.path.join(os.path.dirname(__file__),
                                                  '..', 'templates'),
                                     os.path.join(os.path.dirname(__file__),
                                                  '..', 'outputs'))
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('At a Glance', result[0])

    def test_generate_create_poi_riddle_answers(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        pc = PoiCollection(input_prompts, all_pois)
        result = pc.create_poi_pages(os.path.join(os.path.dirname(__file__),
                                                  '..', 'templates'),
                                     os.path.join(os.path.dirname(__file__),
                                                  '..', 'outputs'))

        print("***Type of riddle answers:", type(pc.all_riddle_answers))
        print(pc.all_riddle_answers)

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_riddlerallyanswers_02.txt',
                  'w', encoding='utf-8') as f:
            f.write(pp.pformat(pc.all_riddle_answers))

        htmlsource = pc.create_poi_riddle_answers(
            os.path.join(os.path.dirname(__file__),
                         '..', 'templates'),
            os.path.join(os.path.dirname(__file__),
                         '..', 'outputs'))

        with open('testfiles/test_riddlerallyanswers_02.html', 'w', encoding='utf-8') as f:
            f.write(htmlsource)

        self.assertIsInstance(htmlsource, str,
                              "HTML source should be a string")
        self.assertGreater(len(htmlsource), 0,
                           "HTML source should not be empty")
        self.assertIn('Riddle Rally Answers', htmlsource)

    def test_create_poi_riddle_answers(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        pc = PoiCollection(input_prompts, all_pois)

        with open("testfiles/test_riddlerallyanswers_03.txt", 'r',
                  encoding='utf-8') as file:
            str_riddle_answers = file.read()
        riddle_answers = ast.literal_eval(str_riddle_answers)

        print("***Type of riddle answers:", type(riddle_answers))
        pc.all_riddle_answers = riddle_answers
        # print(pc.all_riddle_answers)

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_riddlerallyanswers_03.json',
                  'w', encoding='utf-8') as f:
            f.write(pp.pformat(pc.all_riddle_answers))

        htmlsource = pc.create_poi_riddle_answers(
            os.path.join(os.path.dirname(__file__),
                         '..', 'templates'),
            os.path.join(os.path.dirname(__file__),
                         '..', 'outputs'))

        with open('testfiles/test_riddlerallyanswers_03.html', 'w', encoding='utf-8') as f:
            f.write(htmlsource)

        self.assertIsInstance(htmlsource, str,
                              "HTML source should be a string")
        self.assertGreater(len(htmlsource), 0,
                           "HTML source should not be empty")
        self.assertIn('Riddle Rally Answers', htmlsource)


if __name__ == "__main__":
    # Run the test
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestPoiCollection('test_generate_poi_prompt'))
    # suite.addTest(TestPoiCollection('test_generate_create_poi_riddle_answers'))
    suite.addTest(TestPoiCollection('test_create_poi_riddle_answers'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
