import unittest
from src.utils import process_str


class TestUtilFunctions(unittest.TestCase):

    def test_process_str(self):
        text = ' 3.2e-9  '
        processed_text = process_str(text)
        self.assertEqual(processed_text, '3.2e-9')

    def test_empty_str(self):
        text = ''
        processed_text = process_str(text)
        self.assertEqual(processed_text, '')