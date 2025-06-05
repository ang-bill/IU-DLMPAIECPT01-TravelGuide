
import unittest
import ast
import os
import pprint
from itinerary import Itinerary
from input_loader import load_input_prompt_files
from poi import Poi


class TestPoi(unittest.TestCase):
    def test_generate_poi_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = Poi(input_prompts, 'POI-03', all_pois['POI-03'])
        result = p.generate_poi_prompt()

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_prompt_poi_03.txt', 'w', encoding='utf-8') as f:
            f.write(pp.pformat(result))

        self.assertIn('tourist attraction', result)
        self.assertIn('destination_of_trip', result)

    def test_call_api_poi_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = Poi(input_prompts, 'POI-03', all_pois['POI-03'])
        prompt = p.generate_poi_prompt()

        result = p.call_api_poi_prompt(prompt)

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_poi_03.txt', 'w', encoding='utf-8') as f:
            f.write(pp.pformat(result))

        self.assertIsInstance(result, dict,
                              "Response should be a string")
        self.assertGreater(len(result), 0,
                           "Response should not be empty")
        self.assertIn('need_to_know', result)
        self.assertIn('duration', result['overview'])

    def test_retrieve_images(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = Poi(input_prompts, all_pois['POI-03'])
        with open("testfiles/test_poi_03.txt", 'r', encoding='utf-8') as file:
            str_poi_data = file.read()
        poi_data = ast.literal_eval(str_poi_data)
        p.poi_data = poi_data

        image_data = p.retrieve_images()

        self.assertGreater(len(image_data), 0,
                           "Url list should not be empty")
        self.assertIn('https://upload.wikimedia.org', image_data[0]['url'])

    # def test_retrieve_images(self):
    #     i = Itinerary()
    #     with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
    #         str_itinerary_data = file.read()
    #     itinerary_data = ast.literal_eval(str_itinerary_data)
    #     all_pois = i.retrieve_all_pois(itinerary_data)

    #     p = Poi(all_pois['POI-02'])
    #     with open("testfiles/test_poi_02.txt", 'r', encoding='utf-8') as file:
    #         str_poi_data = file.read()
    #     poi_data = ast.literal_eval(str_poi_data)
    #     p.poi_data = poi_data

    #     urls = p.retrieve_image_urls()
    #     self.assertGreater(len(urls), 0,
    #                        "Url list should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', urls[0])

    def test_create_poi(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = Poi(input_prompts, 'POI-03', all_pois['POI-03'])
        with open("testfiles/test_poi_03.txt", 'r', encoding='utf-8') as file:
            str_poi_data = file.read()
        poi_data = ast.literal_eval(str_poi_data)
        p.poi_data = poi_data
        print(poi_data)

        # urls = p.retrieve_image_urls()
        # details = p.retrieve_image_details()
        # print(details)
        images = p.retrieve_images()
        print(images)

        htmlsource = p.create_poi(os.path.join(os.path.dirname(__file__),
                                               '..', 'templates'),
                                  os.path.join(os.path.dirname(__file__),
                                               '..', 'outputs'))
        with open('testfiles/test_poi_03.html', 'w', encoding='utf-8') as f:
            f.write(htmlsource)

        self.assertIsInstance(htmlsource, str,
                              "HTML source should be a string")
        self.assertGreater(len(htmlsource), 0,
                           "HTML source should not be empty")
        self.assertIn('At a Glance', htmlsource)

    def test_retrieve_riddle_answers(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = Poi(input_prompts, 'POI-03', all_pois['POI-03'])
        with open("testfiles/test_poi_03.txt", 'r', encoding='utf-8') as file:
            str_poi_data = file.read()
        poi_data = ast.literal_eval(str_poi_data)
        p.poi_data = poi_data

        dict_riddle_answers = p.retrieve_riddle_answers()

        print("***Type of riddle answers:", type(dict_riddle_answers))
        print(dict_riddle_answers)

        # self.assertIsInstance(dict_riddle_answers, dict,
        #                       "Riddle answer list should be a dict")
        self.assertIsInstance(dict_riddle_answers, list,
                              "Riddle answer list should be a list")
        self.assertGreater(len(dict_riddle_answers), 0,
                           "Riddle answer list should not be empty")
        # self.assertIn('Kreuzgang', dict_riddle_answers[0])
        self.assertIn('Kamp', dict_riddle_answers[0])

    # def test_retrieve_wikimedia_image_url(self):
    #     url_1 = Poi.retrieve_wikimedia_image_url(
    #         "https://commons.wikimedia.org/wiki/File:%C3%96_-_Lilienfeld,_N%C3%96,_280512,_Stift.jpg")
    #     print(url_1)
    #     self.assertGreater(len(url_1), 0,
    #                        "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_1)

    #     url_2 = Poi.retrieve_wikimedia_image_url(
    #         "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftsportal.JPG")
    #     print(url_2)
    #     self.assertGreater(len(url_2), 0,
    #                        "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_2)

    #     url_3 = Poi.retrieve_wikimedia_image_url(
    #         "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftskirche,_Innenansicht.JPG")
    #     print(url_3)
    #     self.assertGreater(len(url_3), 0,
    #                        "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_3)

    # def test_retrieve_image_details(self):
    #     i = Itinerary()
    #     with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
    #         str_itinerary_data = file.read()
    #     itinerary_data = ast.literal_eval(str_itinerary_data)
    #     all_pois = i.retrieve_all_pois(itinerary_data)

    #     p = Poi(all_pois['POI-02'], all_pois['POI-02'])
    #     with open("testfiles/test_poi_02.txt", 'r', encoding='utf-8') as file:
    #         str_poi_data = file.read()
    #     poi_data = ast.literal_eval(str_poi_data)
    #     p.poi_data = poi_data

    #     details = p.retrieve_image_details()
    #     print(details)
    #     # self.assertGreater(len(urls), 0,
    #     #                    "Url list should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', details[0]["image_url"])

    # def test_retrieve_wikimedia_image_detail(self):
    #     url_1 = Poi.retrieve_wikimedia_image_detail(
    #         "https://commons.wikimedia.org/wiki/File:%C3%96_-_Lilienfeld,_N%C3%96,_280512,_Stift.jpg")
    #     # print(url_1)
    #     # self.assertGreater(len(url_1), 0,
    #     #                    "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_1["image_url"])

    #     url_2 = Poi.retrieve_wikimedia_image_detail(
    #         "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftsportal.JPG")
    #     # print(url_2)
    #     # self.assertGreater(len(url_2), 0,
    #     #                    "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_2["image_url"])

    #     url_3 = Poi.retrieve_wikimedia_image_detail(
    #         "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftskirche,_Innenansicht.JPG")
    #     # print(url_3)
    #     # self.assertGreater(len(url_3), 0,
    #     #                    "Url should not be empty")
    #     self.assertIn('https://upload.wikimedia.org', url_3["image_url"])


if __name__ == "__main__":
    # Run the test
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestPoi('test_generate_poi_prompt'))
    # suite.addTest(TestPoi('test_call_api_poi_prompt'))
    suite.addTest(TestPoi('test_create_poi'))
    # suite.addTest(TestPoi('test_retrieve_riddle_answers'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
