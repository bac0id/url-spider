import re

from html_outlinks_parser import HtmlOutlinksParser

class HtmlOutlinksRegexParser(HtmlOutlinksParser):

    def parse(self, html_string):
        if not html_string:
            return []

        #regex = r'<a\s+(?:[^>]*?\s+)?href=(["\']?)(https?://.*?)\1[^>]*?>' # From Google Gemini
        regex = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1' # From https://stackoverflow.com/questions/15926142/

        matches = re.findall(regex, html_string, re.IGNORECASE)

        outlinks = [match[1] for match in matches]

        return outlinks
