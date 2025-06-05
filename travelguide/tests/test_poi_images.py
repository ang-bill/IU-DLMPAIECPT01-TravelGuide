
import unittest
import ast
import os
import pprint
from itinerary import Itinerary
from input_loader import load_input_prompt_files
from poi_images import PoiImages


class TestPoiImages(unittest.TestCase):
    def test_generate_poi_images_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = PoiImages(input_prompts, 'POI-02', all_pois['POI-02'])
        result = p.generate_poi_images_prompt()

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_prompt_poi_02.txt', 'w', encoding='utf-8') as f:
            f.write(pp.pformat(result))

        self.assertIn('tourist attraction', result)
        self.assertIn('wikimedia_urls', result)

    def test_call_api_poi_images_prompt(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = PoiImages(input_prompts, 'POI-02', all_pois['POI-02'])
        prompt = p.generate_poi_images_prompt()

        result = p.call_api_poi_images_prompt(prompt)

        pp = pprint.PrettyPrinter(indent=2, width=120)
        with open('testfiles/test_poi_images_02.txt', 'w', encoding='utf-8') as f:
            f.write(pp.pformat(result))

        self.assertIsInstance(result, dict,
                              "Response should be a string")
        self.assertGreater(len(result), 0,
                           "Response should not be empty")
        self.assertIn('wikimedia_urls', result)
        self.assertIn('https://commons.wikimedia.org',
                      result['wikimedia_urls'][0])

    def test_retrieve_image_details(self):
        input_prompts = load_input_prompt_files("../prompts")
        i = Itinerary(input_prompts)
        with open("testfiles/test_itinerary_01.txt", 'r', encoding='utf-8') as file:
            str_itinerary_data = file.read()
        itinerary_data = ast.literal_eval(str_itinerary_data)
        all_pois = i.retrieve_all_pois(itinerary_data)

        p = PoiImages(input_prompts, all_pois['POI-02'], all_pois['POI-02'])
        with open("testfiles/test_poi_images_02_existing.txt", 'r', encoding='utf-8') as file:
            str_poi_data = file.read()
        images = ast.literal_eval(str_poi_data)
        p.images = images

        details = p.retrieve_image_details()
        print("*** Image Details ***")
        print(details)
        # self.assertGreater(len(urls), 0,
        #                    "Url list should not be empty")
        self.assertIn('https://upload.wikimedia.org', details[0]["image_url"])

    def test_retrieve_wikimedia_image_detail(self):
        detail_1 = PoiImages.retrieve_wikimedia_image_detail(
            "https://commons.wikimedia.org/wiki/File:%C3%96_-_Lilienfeld,_N%C3%96,_280512,_Stift.jpg")
        print(detail_1)
        # self.assertGreater(len(url_1), 0,
        #                    "Url should not be empty")
        self.assertIn('https://upload.wikimedia.org', detail_1["image_url"])

        detail_2 = PoiImages.retrieve_wikimedia_image_detail(
            "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftsportal.JPG")
        print(detail_2)
        # self.assertGreater(len(url_2), 0,
        #                    "Url should not be empty")
        self.assertIn('https://upload.wikimedia.org', detail_2["image_url"])

        detail_3 = PoiImages.retrieve_wikimedia_image_detail(
            "https://commons.wikimedia.org/wiki/File:Lilienfeld_-_Stiftskirche,_Innenansicht.JPG")
        print(detail_3)
        # self.assertGreater(len(url_3), 0,
        #                    "Url should not be empty")
        self.assertIn('https://upload.wikimedia.org', detail_3["image_url"])


if __name__ == "__main__":
    # Run the test
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestPoiImages('test_generate_poi_images_prompt'))
    # suite.addTest(TestPoiImages('test_call_api_poi_images_prompt'))
    # suite.addTest(TestPoiImages('test_retrieve_image_details'))
    suite.addTest(TestPoiImages('test_retrieve_wikimedia_image_detail'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
