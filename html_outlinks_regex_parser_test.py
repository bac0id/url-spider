import unittest

from html_outlinks_regex_parser import HtmlOutlinksRegexParser

class HtmlOutlinksRegexParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = HtmlOutlinksRegexParser()

    def test_empty_html(self):
        self.assertEqual(self.parser.parse(""), [])

    def test_no_links(self):
        html = "<html><body><p>No links here</p></body></html>"
        self.assertEqual(self.parser.parse(html), [])

    def test_single_link_double_quotes(self):
        html = '<a href="https://www.google.com">Google</a>'
        self.assertEqual(self.parser.parse(html), ["https://www.google.com"])

    def test_single_link_single_quotes(self):
        html = "<a href='http://www.bing.com'>Bing</a>"
        self.assertEqual(self.parser.parse(html), ["http://www.bing.com"])

    def test_single_link_to_file(self):
        html = "<a href='http://www.bing.com/index.html'>Bing</a>"
        self.assertEqual(self.parser.parse(html), ["http://www.bing.com/index.html"])

    # def test_single_link_no_quotes(self):
    #     html = "<a href=http://www.yahoo.com>Yahoo</a>"
    #     self.assertEqual(self.parser.parse(html), ["http://www.yahoo.com"])

    def test_multiple_links(self):
        html = """
        <a href="https://www.google.com">Google</a>
        <a href='http://www.bing.com'>Bing</a>
        """
        expected_links = ["https://www.google.com", "http://www.bing.com"]
        self.assertEqual(self.parser.parse(html), expected_links)

    def test_link_with_parameters(self):
        html = '<a href="https://www.example.net/path?param=value">url_with_param</a>'
        self.assertEqual(self.parser.parse(html), ["https://www.example.net/path?param=value"])

    def test_link_with_other_attributes(self):
      html = '<a target="_blank" rel="noopener noreferrer" href="https://www.example.com">Example</a>'
      self.assertEqual(self.parser.parse(html), ["https://www.example.com"])

    def test_mixed_quotes(self):
        html = """
        <a href="https://www.google.com">Google</a>
        <a href='http://www.bing.com'>Bing</a>
        <a href="https://www.example.net/path?param=value">url_with_param</a>
        <a target="_blank" href="https://www.example.com">Example</a>
        """
        expected_links = [
            "https://www.google.com",
            "http://www.bing.com",
            "https://www.example.net/path?param=value",
            "https://www.example.com",
        ]
        self.assertEqual(self.parser.parse(html), expected_links)
    
    def test_javascript_link(self):
        html = '<a href="javascript:void(0);">JavaScript Link</a>'
        self.assertEqual(self.parser.parse(html), ["javascript:void(0);"])

    def test_mailto_link(self):
        html = '<a href="mailto:test@example.com">mailto_link</a>'
        self.assertEqual(self.parser.parse(html), ["mailto:test@example.com"])

    def test_mailto_link_for_multiple_recipients(self):
        html = '<a href="mailto:recipient1@example.com, recipient2@example.com">mailto_link_for_multiple_recipients</a>'
        self.assertEqual(self.parser.parse(html), ["mailto:recipient1@example.com, recipient2@example.com"])

    def test_uppercase_https(self):
        html = '<a href="HTTPS://www.UPPERCASE.com">uppercase</a>'
        self.assertEqual(self.parser.parse(html), ["HTTPS://www.UPPERCASE.com"])

    # def test_link_with_leading_and_trailing_spaces_in_href(self):
    #     html = '<a href="  https://www.example.com  ">Example</a>'
    #     self.assertEqual(self.parser.parse(html), ["  https://www.example.com  "])

    def test_link_with_internal_spaces_in_href(self):
        html = '<a href="https://www.exam ple.com">Example</a>'
        self.assertEqual(self.parser.parse(html), ["https://www.exam ple.com"])

    # def test_link_with_new_lines_in_href(self):
    #     html = '<a href="https://www.\nexample.com">Example</a>'
    #     self.assertEqual(self.parser.parse(html), ["https://www.\nexample.com"])

    def test_link_with_tab_in_href(self):
        html = '<a href="https://www.\texample.com">Example</a>'
        self.assertEqual(self.parser.parse(html), ["https://www.\texample.com"])

    def test_no_closing_tag(self):
        html = '<a href="https://www.example.com"'
        self.assertEqual(self.parser.parse(html), ["https://www.example.com"])

    def test_invalid_html(self):
        html = '<a href="https://www.example.com">text<b>'
        self.assertEqual(self.parser.parse(html), ["https://www.example.com"])

    def test_link_with_special_characters(self):
        html = '<a href="https://www.example.com/path?param=val&other=val2">Special Chars</a>'
        self.assertEqual(self.parser.parse(html), ["https://www.example.com/path?param=val&other=val2"])


if __name__ == '__main__':
    unittest.main()
