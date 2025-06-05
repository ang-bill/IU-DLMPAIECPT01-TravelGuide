
import unittest
import input_loader


class TestInputLoader(unittest.TestCase):
    def test_load_input_prompt_files_empty(self):
        prompts = input_loader.load_input_prompt_files('../prompts')
        self.assertIsInstance(prompts, dict)


if __name__ == "__main__":
    # Run the test
    unittest.main()
