import unittest

from outlink_converter import to_absolute_url

class TestToAbsoluteUrl(unittest.TestCase):

    def test_relative_url(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "another_page.html"
        expected = "https://www.example.com/path/another_page.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_absolute_path(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "/absolute_path.html"
        expected = "https://www.example.com/absolute_path.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_already_absolute_url(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "https://www.google.com"
        expected = "https://www.google.com"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_parent_directory(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "../parent_page.html"
        expected = "https://www.example.com/parent_page.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_current_directory(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "./another_page.html"
        expected = "https://www.example.com/path/another_page.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_invalid_base_url(self):
        base_url = "invalid_base_url"
        outlink = "outlink"
        self.assertIsNone(to_absolute_url(base_url, outlink))

    def test_empty_outlink(self):
        base_url = "https://www.example.com"
        outlink = ""
        self.assertIsNone(to_absolute_url(base_url, outlink))

    def test_empty_base_url(self):
        base_url = ""
        outlink = "outlink"
        expected = "outlink"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)
    
    def test_mailto_link(self):
        base_url = "https://www.example.com"
        outlink = "mailto:test@example.com"
        expected = "mailto:test@example.com"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_fragment(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "#fragment"
        expected = "https://www.example.com/path/page.html#fragment"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_base_url_with_fragment(self):
        base_url = "https://www.example.com/path/page.html#test"
        outlink = "/absolute_path.html"
        expected = "https://www.example.com/absolute_path.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_base_url_with_query(self):
        base_url = "https://www.example.com/path/page.html?test=1"
        outlink = "/absolute_path.html"
        expected = "https://www.example.com/absolute_path.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)
    
    def test_double_slash_outlink(self):
        base_url = "https://www.example.com/path/page.html"
        outlink = "//www.test.com"
        expected = "https://www.test.com"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_base_url_with_trailing_slash_and_relative_outlink(self):
        base_url = "https://www.example.com/path/"
        outlink = "another_page.html"
        expected = "https://www.example.com/path/another_page.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_base_url_without_trailing_slash_and_relative_outlink(self):
        base_url = "https://www.example.com/path"
        outlink = "another_page.html"
        expected = "https://www.example.com/another_page.html"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)

    def test_outlink_with_special_characters(self):
        base_url = "https://www.example.com"
        outlink = "my#page?param=val"
        expected = "https://www.example.com/my#page?param=val"
        self.assertEqual(to_absolute_url(base_url, outlink), expected)


if __name__ == '__main__':
    unittest.main()
