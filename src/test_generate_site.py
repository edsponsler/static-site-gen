import unittest
from generate_site import extract_title

class TestGenerateSite(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_multiline(self):
        markdown = """This is some text
# The Real Title
More text underneath"""
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_extract_title_missing_raises_error(self):
        markdown = """This is some text
## Not an h1 title
More text underneath"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty_string_raises_error(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
