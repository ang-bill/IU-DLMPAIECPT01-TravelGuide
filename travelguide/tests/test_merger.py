
import unittest
import os
import merger


class TestMerger(unittest.TestCase):
    def test_merge_all_pages(self):
        merger.merge_all_pages(os.path.join(os.path.dirname(
            __file__), '..', 'outputs'))

        # self.assertIsInstance(htmlsource, str,
        #                       "HTML source should be a string")
        # self.assertGreater(len(htmlsource), 0,
        #                    "HTML source should not be empty")
        # self.assertIn('Route Description', htmlsource)

        # Assert that the file exists
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(
            __file__), '..', 'outputs/travelguide.pdf')),
            "outputs/travelguide.pdf was not created.")


if __name__ == "__main__":
    # Run the test
    unittest.main()
